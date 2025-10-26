#!/usr/bin/env python3
"""
Binary Encoding System for Dashboard Communication

This module provides a clean way to encode and decode dashboard messages
using binary strings instead of fragile text parsing.
"""

# Message type definitions
MESSAGE_TYPES = {
    'PLAYER_CONNECT': '0001',
    'PLAYER_DISCONNECT': '0010', 
    'TOURNAMENT_START': '0011',
    'TOURNAMENT_END': '0100',
    'ROUND_UPDATE': '0101',
    'RESULTS_SAVED': '0110',
    'LEADERBOARD_START': '0111',
    'LEADERBOARD_ENTRY': '1000',
    'SERVER_STATUS': '1001',
    'ERROR': '1010'
}

# Reverse lookup for decoding
TYPE_FROM_BINARY = {v: k for k, v in MESSAGE_TYPES.items()}

def encode_message(message_type: str, data: dict) -> str:
    """
    Encode a dashboard message as a binary string.
    
    Args:
        message_type: One of the MESSAGE_TYPES keys
        data: Dictionary containing the message data
        
    Returns:
        Binary string in format "encoded:10010001010"
    """
    if message_type not in MESSAGE_TYPES:
        raise ValueError(f"Unknown message type: {message_type}")
    
    # Start with the message type
    binary = MESSAGE_TYPES[message_type]
    
    # Encode data fields based on message type
    if message_type == 'PLAYER_CONNECT':
        # Format: player_name|address
        player_name = data.get('player_name', '')
        address = data.get('address', '')
        binary += encode_string(player_name) + encode_string(address)
        
    elif message_type == 'PLAYER_DISCONNECT':
        # Format: player_name|remaining_count
        player_name = data.get('player_name', '')
        remaining_count = str(data.get('remaining_count', 0))
        binary += encode_string(player_name) + encode_string(remaining_count)
        
    elif message_type == 'TOURNAMENT_START':
        # Format: game_type|player_count
        game_type = data.get('game_type', '')
        player_count = str(data.get('player_count', 0))
        binary += encode_string(game_type) + encode_string(player_count)
        
    elif message_type == 'TOURNAMENT_END':
        # Format: game_type
        game_type = data.get('game_type', '')
        binary += encode_string(game_type)
        
    elif message_type == 'ROUND_UPDATE':
        # Format: current_round|total_rounds
        current_round = str(data.get('current_round', 0))
        total_rounds = str(data.get('total_rounds', 0))
        binary += encode_string(current_round) + encode_string(total_rounds)
        
    elif message_type == 'RESULTS_SAVED':
        # Format: filename
        filename = data.get('filename', '')
        binary += encode_string(filename)
        
    elif message_type == 'LEADERBOARD_START':
        # Format: game_type
        game_type = data.get('game_type', '')
        binary += encode_string(game_type)
        
    elif message_type == 'LEADERBOARD_ENTRY':
        # Format: rank|name|total|games|avg
        rank = str(data.get('rank', 0))
        name = data.get('name', '')
        total = str(data.get('total', 0))
        games = str(data.get('games', 0))
        avg = str(data.get('avg', 0))
        binary += encode_string(rank) + encode_string(name) + encode_string(total) + encode_string(games) + encode_string(avg)
        
    elif message_type == 'SERVER_STATUS':
        # Format: status|uptime|players
        status = data.get('status', '')
        uptime = data.get('uptime', '')
        players = str(data.get('players', 0))
        binary += encode_string(status) + encode_string(uptime) + encode_string(players)
        
    elif message_type == 'ERROR':
        # Format: error_message
        error_message = data.get('error_message', '')
        binary += encode_string(error_message)
    
    return f"encoded:{binary}"

def decode_message(encoded_line: str) -> tuple:
    """
    Decode a binary encoded dashboard message.
    
    Args:
        encoded_line: Line starting with "encoded:" followed by binary string
        
    Returns:
        Tuple of (message_type, data_dict) or (None, None) if invalid
    """
    if not encoded_line.startswith("encoded:"):
        return None, None
    
    try:
        binary = encoded_line[8:]  # Remove "encoded:" prefix
        
        if len(binary) < 4:
            return None, None
            
        # Extract message type (first 4 bits)
        message_type_binary = binary[:4]
        message_type = TYPE_FROM_BINARY.get(message_type_binary)
        
        if not message_type:
            return None, None
        
        # Extract data based on message type
        data = {}
        remaining_binary = binary[4:]
        
        if message_type == 'PLAYER_CONNECT':
            player_name, remaining_binary = decode_string(remaining_binary)
            address, remaining_binary = decode_string(remaining_binary)
            data = {'player_name': player_name, 'address': address}
            
        elif message_type == 'PLAYER_DISCONNECT':
            player_name, remaining_binary = decode_string(remaining_binary)
            remaining_count, remaining_binary = decode_string(remaining_binary)
            data = {'player_name': player_name, 'remaining_count': int(remaining_count)}
            
        elif message_type == 'TOURNAMENT_START':
            game_type, remaining_binary = decode_string(remaining_binary)
            player_count, remaining_binary = decode_string(remaining_binary)
            data = {'game_type': game_type, 'player_count': int(player_count)}
            
        elif message_type == 'TOURNAMENT_END':
            game_type, remaining_binary = decode_string(remaining_binary)
            data = {'game_type': game_type}
            
        elif message_type == 'ROUND_UPDATE':
            current_round, remaining_binary = decode_string(remaining_binary)
            total_rounds, remaining_binary = decode_string(remaining_binary)
            data = {'current_round': int(current_round), 'total_rounds': int(total_rounds)}
            
        elif message_type == 'RESULTS_SAVED':
            filename, remaining_binary = decode_string(remaining_binary)
            data = {'filename': filename}
            
        elif message_type == 'LEADERBOARD_START':
            game_type, remaining_binary = decode_string(remaining_binary)
            data = {'game_type': game_type}
            
        elif message_type == 'LEADERBOARD_ENTRY':
            rank, remaining_binary = decode_string(remaining_binary)
            name, remaining_binary = decode_string(remaining_binary)
            total, remaining_binary = decode_string(remaining_binary)
            games, remaining_binary = decode_string(remaining_binary)
            avg, remaining_binary = decode_string(remaining_binary)
            data = {'rank': int(rank), 'name': name, 'total': float(total), 'games': int(games), 'avg': float(avg)}
            
        elif message_type == 'SERVER_STATUS':
            status, remaining_binary = decode_string(remaining_binary)
            uptime, remaining_binary = decode_string(remaining_binary)
            players, remaining_binary = decode_string(remaining_binary)
            data = {'status': status, 'uptime': uptime, 'players': int(players)}
            
        elif message_type == 'ERROR':
            error_message, remaining_binary = decode_string(remaining_binary)
            data = {'error_message': error_message}
        
        return message_type, data
        
    except Exception:
        return None, None

def encode_string(s: str) -> str:
    """
    Encode a string as binary with length prefix.
    
    Args:
        s: String to encode
        
    Returns:
        Binary string with length prefix
    """
    # Convert string to bytes
    s_bytes = s.encode('utf-8')
    
    # Encode length as 8-bit binary
    length = len(s_bytes)
    length_binary = format(length, '08b')
    
    # Encode string bytes as binary
    string_binary = ''.join(format(byte, '08b') for byte in s_bytes)
    
    return length_binary + string_binary

def decode_string(binary: str) -> tuple:
    """
    Decode a binary string back to original string.
    
    Args:
        binary: Binary string with length prefix
        
    Returns:
        Tuple of (decoded_string, remaining_binary)
    """
    if len(binary) < 8:
        return "", binary
    
    # Extract length (first 8 bits)
    length_binary = binary[:8]
    length = int(length_binary, 2)
    
    # Calculate total bits needed
    total_bits = 8 + (length * 8)
    
    if len(binary) < total_bits:
        return "", binary
    
    # Extract string bytes
    string_binary = binary[8:total_bits]
    remaining = binary[total_bits:]
    
    # Convert binary back to string
    try:
        # Convert binary to bytes
        bytes_list = []
        for i in range(0, len(string_binary), 8):
            byte_binary = string_binary[i:i+8]
            if len(byte_binary) == 8:
                bytes_list.append(int(byte_binary, 2))
        
        # Decode bytes to string
        decoded_string = bytes(bytes_list).decode('utf-8')
        return decoded_string, remaining
        
    except Exception:
        return "", remaining

# Convenience functions for common messages
def encode_player_connect(player_name: str, address: str) -> str:
    """Encode a player connection message."""
    return encode_message('PLAYER_CONNECT', {
        'player_name': player_name,
        'address': address
    })

def encode_player_disconnect(player_name: str, remaining_count: int) -> str:
    """Encode a player disconnection message."""
    return encode_message('PLAYER_DISCONNECT', {
        'player_name': player_name,
        'remaining_count': remaining_count
    })

def encode_tournament_start(game_type: str, player_count: int) -> str:
    """Encode a tournament start message."""
    return encode_message('TOURNAMENT_START', {
        'game_type': game_type,
        'player_count': player_count
    })

def encode_tournament_end(game_type: str) -> str:
    """Encode a tournament end message."""
    return encode_message('TOURNAMENT_END', {
        'game_type': game_type
    })

def encode_round_update(current_round: int, total_rounds: int) -> str:
    """Encode a round update message."""
    return encode_message('ROUND_UPDATE', {
        'current_round': current_round,
        'total_rounds': total_rounds
    })

def encode_results_saved(filename: str) -> str:
    """Encode a results saved message."""
    return encode_message('RESULTS_SAVED', {
        'filename': filename
    })

def encode_leaderboard_start(game_type: str) -> str:
    """Encode a leaderboard start message."""
    return encode_message('LEADERBOARD_START', {
        'game_type': game_type
    })

def encode_leaderboard_entry(rank: int, name: str, total: float, games: int, avg: float) -> str:
    """Encode a leaderboard entry message."""
    return encode_message('LEADERBOARD_ENTRY', {
        'rank': rank,
        'name': name,
        'total': total,
        'games': games,
        'avg': avg
    })

# Test functions
def test_encoding():
    """Test the encoding/decoding system."""
    print("Testing binary encoding system...")
    
    # Test player connect
    encoded = encode_player_connect("Player1", "127.0.0.1:12345")
    print(f"Encoded: {encoded}")
    
    message_type, data = decode_message(encoded)
    print(f"Decoded: {message_type}, {data}")
    
    # Test tournament start
    encoded = encode_tournament_start("rps", 2)
    print(f"Encoded: {encoded}")
    
    message_type, data = decode_message(encoded)
    print(f"Decoded: {message_type}, {data}")

if __name__ == "__main__":
    test_encoding()
