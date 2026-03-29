"""Shared in-memory data store for AutoSME MVP."""
from typing import List, Dict
import uuid
from datetime import datetime

# Products
products: List[Dict] = []

# Orders
orders: List[Dict] = []

# Tasks
tasks: List[Dict] = []

# Opt-out set for WhatsApp
optout_phones: set = set()