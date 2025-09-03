# stages/adx_offline_stage.py
from __future__ import annotations
import math
import numpy as np
import random
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any

from core.stage.BaseStage import BaseStage
from core.game import PlayerId, ObsDict, ActionDict, RewardDict, InfoDict



SegmentId = int

@dataclass
class BidBundle:
    """One-shot submission for 26 segments."""
    bids: Dict[SegmentId, float]           # CPM bids
    limits: Dict[SegmentId, int]           # max impressions per seg
    budget: float                          # campaign budget (money)
    reach_goal: int                        # required impressions
    # internal bookkeeping (not sent by agent)
    spend: float = 0.0
    hit: Dict[SegmentId, int] = field(default_factory=lambda: {s: 0 for s in range(26)})

histograms = {
    seg: np.random.beta(a=2, b=5, size=10000) * 15  # toy per‑segment CPM draws
    for seg in range(26)
}

def rival_sampler_by_hist(seg_id: int):
    return float(np.random.choice(histograms[seg_id]))

class AdxOfflineStage(BaseStage):
    """
    One-day TAC-AdX simulation.

    Parameters
    ----------
    num_players : int
        External agents (1 locally, 26 in competition).
    day_idx : int
        0 for Day-1, 1 for Day-2 (used to scale budget via QC).
    qc_multiplier : float
        Quality-score multiplier applied to **budget** *and* objective in Day-2.
    rival_sampler : callable
        Function: seg_id → rival CPM bid distribution sampler.  Defaults to U[0,10].
    n_auctions : int
        How many impression auctions constitute a "day".  Default 10,000.
    """

    SEGMENTS = list(range(26))

    def __init__(
        self,
        num_players: int,
        day_idx: int,
        qc_multiplier: float = 1.0,
        rival_sampler=None,
        n_auctions: int = 10_000, #this is cool I didn't know I could do this :D
    ):
        super().__init__(num_players)
        self.day = day_idx
        self.qc = qc_multiplier
        self.n_auctions = n_auctions
        self.rival_sampler = rival_sampler or rival_sampler_by_hist
        self._bundle: Dict[PlayerId, BidBundle] = {}
        self._done_once = False






    def legal_actions(self, _pid):
        return "BidBundle dataclass with bids[0-25], limits[0-25], budget, reach_goal"



    def step(
        self,
        actions: ActionDict
    ) -> Tuple[ObsDict, RewardDict, bool, InfoDict]:
        print(f"[STAGE DEBUG] AdxOfflineStage.step() called with actions: {actions}", flush=True)
        print(f"[STAGE DEBUG] Day: {self.day}, QC multiplier: {self.qc}, n_auctions: {self.n_auctions}", flush=True)
        
        # Validate: one bundle per external agent exactly once
        if self._done_once:
            print(f"[STAGE DEBUG] Error: Bundles already submitted", flush=True)
            raise RuntimeError("Bundles already submitted")
        
        #validate actions
        print(f"[STAGE DEBUG] Validating actions...", flush=True)
        self._validate_actions(actions)
        print(f"[STAGE DEBUG] Actions validated successfully", flush=True)

        self._bundle = actions  # keep reference
        print(f"[STAGE DEBUG] Running simulation with {self.n_auctions} auctions...", flush=True)
        self._run_simulation()
        print(f"[STAGE DEBUG] Simulation completed", flush=True)

        reward: RewardDict = {}
        info: InfoDict = {}
        for pid, bundle in self._bundle.items():
            reach_hit = sum(bundle.hit.values())
            profit = min(reach_hit / bundle.reach_goal, 1.0) * (bundle.budget) - bundle.spend
            reward[pid] = profit
            info[pid] = {
                "spend": bundle.spend,
                "reach_hit": reach_hit,
            }
            if self.day == 0:
                qc_score = self._quality_score(reach_hit, bundle.reach_goal)
                info[pid]["qc"] = qc_score
                print(f"[STAGE DEBUG] Player {pid} QC score: {qc_score} (reach_hit: {reach_hit}, goal: {bundle.reach_goal})", flush=True)
            
            print(f"[STAGE DEBUG] Player {pid} results: reach_hit={reach_hit}, spend={bundle.spend}, profit={profit}", flush=True)

        self._done = True
        self._done_once = True
        obs: ObsDict = {pid: {} for pid in actions}
        print(f"[STAGE DEBUG] step() returning: obs={obs}, reward={reward}, done=True, info={info}", flush=True)
        return obs, reward, True, info

    # ------------ internal helpers ----------------------------------

    def _run_simulation(self):
        """Toy simulator: each auction draws a random segment and rival price."""
        print(f"[STAGE DEBUG] Starting simulation with {self.n_auctions} auctions", flush=True)
        print(f"[STAGE DEBUG] Bundles: {self._bundle}", flush=True)
        
        for auction_num in range(self.n_auctions): 
            seg = random.choice(self.SEGMENTS) #uniformly draw a segment
            rival_price = self.rival_sampler(seg) #get rival price

            # determine best external bid
            best_pid, best_bid = None, -1.0
            for pid, bundle in self._bundle.items():
                bid = bundle.bids.get(seg, 0.0)
                if bid > best_bid and bundle.hit[seg] < bundle.limits.get(seg, 0):
                    best_pid, best_bid = pid, bid

            # winner?
            if best_pid is not None and best_bid > rival_price:
                # pay rival_price (2nd price)
                bundle = self._bundle[best_pid]
                bundle.spend += rival_price / 1000.0            # CPM -> per-impression
                bundle.hit[seg] += 1
                
                # Log every 1000th auction for debugging
                if auction_num % 1000 == 0:
                    print(f"[STAGE DEBUG] Auction {auction_num}: segment {seg}, rival_price={rival_price:.3f}, winner={best_pid}, bid={best_bid:.3f}", flush=True)
        
        print(f"[STAGE DEBUG] Simulation completed. Final bundle states:", flush=True)
        for pid, bundle in self._bundle.items():
            print(f"[STAGE DEBUG] Player {pid}: spend={bundle.spend:.3f}, hits={bundle.hit}", flush=True)

    def _quality_score(self, reach: int, goal: int) -> float:
        """
        Calculate quality score using the formula from the writeup.
        
        QC(x) = (2/a) * (arctan(a * (x/R - b)) - arctan(-b)) + 1
        where a = 4.08577, b = 3.08577, x = impressions achieved, R = campaign reach
        
        This produces:
        - QC(0) ≈ 0.89 (low quality)
        - QC(R) ≈ 0.90 (good quality) 
        - QC(∞) ≈ 1.38 (perfect quality)
        """
        a = 4.08577
        b = 3.08577
        x = reach
        R = goal
        
        if R == 0:
            return 0.0
            
        x_over_R = x / R
        quality_score = (2 / a) * (math.atan(a * (x_over_R - b)) - math.atan(-b)) + 1
        
        return max(0.0, quality_score)  # Ensure non-negative

