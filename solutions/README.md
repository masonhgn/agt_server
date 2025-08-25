# Lab 2 Solutions

This directory contains working implementations of all the Lab 2 agents for reference.

## Files

- `bos_competition_agent.py` - Working implementation of the main BOS competition agent
- `bos_finite_state_agent1.py` - Working implementation of FSM agent to counter "reluctant to compromise" strategy
- `bos_finite_state_agent2.py` - Working implementation of FSM agent to counter "punitive" strategy  
- `bosii_competition_agent.py` - Working implementation of the BOSII competition agent with all helper methods
- `bos_reluctant.py` - Implementation of the "reluctant to compromise" strategy
- `bos_punitive.py` - Implementation of the "punitive" strategy

## Testing

You can test any of these agents by running them directly:

```bash
python bos_competition_agent.py
python bos_finite_state_agent1.py
python bos_finite_state_agent2.py
python bosii_competition_agent.py
```

Each agent includes local testing code that will run when executed directly.

## Note

These are reference implementations. Students should implement their own strategies in the main stencil files.
