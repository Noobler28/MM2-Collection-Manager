# lists.py

# Rarity Colours
RARITY_COLOURS = {
    "Common": "gray",
    "Uncommon": "turquoise",
    "Rare": "green",
    "Legendary": "red",
    "Godly": "hotpink",
    "Unique": "#DAA520",
    "Vintage": "gold", 
    "Chroma": "blue",
    "Ancient": "purple",
}
# Chroma Colours
CHROMA_COLOURS = [
    "#FF0000",  # Red
    "#FF7F00",  # Orange
    "#DAA520",  # Yellow
    "#00FF00",  # Green
    "#0000FF",  # Blue
    "#4B0082",  # Indigo
    "#9400D3"   # Violet
]

# Weapons List (Same As .JSON)
weapons = {
    "Mystery Boxes": {
        "Mystery Box 1": {
            "Knife": {
                "Combat": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Copper": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Hardened": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Camo": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Tiger": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Space": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Rune": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Gemstone": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Gemstone": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            },
            "Gun": {
                "Splat": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Pirate": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Rainbow": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"}
            }
        },
        "Mystery Box 2": {
            "Knife": {
                "Shaded": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Lovely": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Leaf": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Graffiti": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "High Tech": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Deep Sea": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"}
            },
            "Gun": {
                "Clown": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "BioGun": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Nightfire": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Splash": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Lightbringer": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Darkbringer": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Lightbringer": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"},
                "Chroma Darkbringer": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Knife Box 1": {
            "Knife": {
                "Whiteout": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Splatter": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Ice": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Love": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Bluesteel": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Adurite": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Wanwood": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Rainbow": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Galaxy": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Plasmite": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Deathshard": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Deathshard": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Knife Box 2": {
            "Knife": {
                "Linked": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Slate": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Borders": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "8bit": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Stalker": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Missing": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Cheesy": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Krypto": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Spectrum": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Overseer": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Fang": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Fang": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Knife Box 3": {
            "Knife": {
                "Clan": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Cherry": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Cardboard": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Stainless": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Circuit": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Doge": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Paper": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Nova": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Vortex": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Splash": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Saw": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Saw": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Knife Box 4": {
            "Knife": {
                "Bleached": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Clown": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Aqua": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Oily": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Hazmat": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Melon": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Hive": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Korblox": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Squire": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Fade": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Slasher": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Slasher": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Knife Box 5": {
            "Knife": {
                "Eco": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Log": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Sandy": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Static": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Brush": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Jigsaw": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Lucky": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Abstract": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Musical": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Fusion": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Tides": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Tides": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Rainbow Box": {
            "Knife": {
                "Brown": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Orange": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Yellow": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Green": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Pink": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Blue": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Red": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Black": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Purple": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Shiny": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Heat": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Heat": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Gun Box 1": {
            "Gun": {
                "Iron": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Fallout": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Cold": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Big Kill": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Bluesteel": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Adurite": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Camo": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Imbued": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Galactic": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Viper": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Luger": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Luger": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Gun Box 2": {
            "Gun": {
                "Engraved": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Infiltrator": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Juice": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Star": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Sketch": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Marina": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Cheddar": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "iRevolver": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Hacker": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Predator": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Shark": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Shark": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        },
        "Gun Box 3": {
            "Gun": {
                "Bit": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Pea": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "News": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "HL2": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Caution": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Soda": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Wooden": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Ace": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Bacon": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Universe": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Laser": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Chroma Laser": {"Status": "Not Collected", "Count": 0, "Rarity": "Chroma"}
            }
        }
    },
    "Events": {
        "Christmas Event 2015": {
            "Knife": {
                "Chill": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Handsaw": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Xmas": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Santa": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Elf": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Ornament1": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Ornament2": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Snowy": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Snowman": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Wrapped": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Ginger": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Cane": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Tree": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"}
            },
            "Gun": {
                "Red Luger": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Green Luger": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Santa": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Elf": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Ornament1": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Ornament2": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Snowy": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Snowman": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Wrapped": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Ginger": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Cane": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Tree": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"}
            }
        },
        "Christmas Event 2016": {
            "Knife": {
                "Ice Dragon": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"}
            }
        },
        "Christmas Event 2017": {
            "Knife": {
                "Frostsaber": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Snowflake": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Present": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Coal": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Elf": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Santa": {"Status": "Not Collected", "Count": 0, "Rarity": "Common"},
                "Frosty": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Sweater": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Tree": {"Status": "Not Collected", "Count": 0, "Rarity": "Uncommon"},
                "Gingerbread": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Snowy": {"Status": "Not Collected", "Count": 0, "Rarity": "Rare"},
                "Green Fire": {"Status": "Not Collected", "Count": 0, "Rarity": "Legendary"},
                "Winter's Edge": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"},
                "Blue Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Unique"},
                "Bronze Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Unique"},
                "Silver Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Unique"},
                "Gold Candy": {"Status": "Not Collected", "Count": 0, "Rarity": "Unique"},
                "Ice Shard": {"Status": "Not Collected", "Count": 0, "Rarity": "Godly"}
            }
        }
    }
}

