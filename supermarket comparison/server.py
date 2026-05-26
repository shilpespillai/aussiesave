import http.server
import socketserver
import urllib.parse
import json
import os
import random
import sys
import time
import datetime
import threading
import subprocess

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# ──────────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE AUSTRALIAN SUPERMARKET PRODUCT CATALOG
# ──────────────────────────────────────────────────────────────────────────────
# Each entry: { "name", "brand", "size", "base_price", "category" }
CATALOG = {

    # ── LAUNDRY ──────────────────────────────────────────────────────────────
    "laundry": [
        {"name": "Dynamo Professional Laundry Liquid 1.8L",    "brand": "Dynamo",         "size": "1.8L",  "base_price": 27.00},
        {"name": "Omo Active Clean Laundry Liquid 2L",         "brand": "Omo",            "size": "2L",    "base_price": 24.00},
        {"name": "Cold Power Regular Laundry Liquid 2L",       "brand": "Cold Power",     "size": "2L",    "base_price": 26.00},
        {"name": "Biozet Attack Regular Laundry Powder 2kg",   "brand": "Biozet Attack",  "size": "2kg",   "base_price": 24.00},
        {"name": "Radiant Colour Care Laundry Liquid 2L",      "brand": "Radiant",        "size": "2L",    "base_price": 20.00},
        {"name": "Fab Essential Laundry Liquid 2L",            "brand": "Fab",            "size": "2L",    "base_price": 12.00},
        {"name": "Surf Tropical Fresh Laundry Powder 2kg",     "brand": "Surf",           "size": "2kg",   "base_price": 8.50},
        {"name": "Persil ProClean Sensitive Laundry 2L",       "brand": "Persil",         "size": "2L",    "base_price": 18.00},
        {"name": "Woolworths Everyday Laundry Liquid 2L",      "brand": "Woolworths",     "size": "2L",    "base_price": 3.50},
        {"name": "Coles Smart Buy Laundry Powder 1kg",         "brand": "Coles",          "size": "1kg",   "base_price": 2.90},
        {"name": "ALDI Almat Laundry Liquid 2L",               "brand": "Almat (ALDI)",   "size": "2L",    "base_price": 3.49},
        {"name": "Napisan Stain Remover Laundry Soaker 1kg",   "brand": "Napisan",        "size": "1kg",   "base_price": 9.00},
        {"name": "Cold Power Advanced Clean Pods 20pk",        "brand": "Cold Power",     "size": "20pk",  "base_price": 14.00},
        {"name": "Omo Ultimate Front Loader 2kg",              "brand": "Omo",            "size": "2kg",   "base_price": 28.00},
    ],

    # ── DISHWASHING ───────────────────────────────────────────────────────────
    "dishwashing": [
        {"name": "Morning Fresh Original Dishwashing Liquid 900mL", "brand": "Morning Fresh", "size": "900mL", "base_price": 5.50},
        {"name": "Finish Quantum Dishwasher Tabs 36pk",         "brand": "Finish",         "size": "36pk",  "base_price": 16.00},
        {"name": "Fairy Platinum Dishwasher Tabs 40pk",         "brand": "Fairy",          "size": "40pk",  "base_price": 18.00},
        {"name": "Sunlight Lemon Dishwashing Liquid 1L",        "brand": "Sunlight",       "size": "1L",    "base_price": 3.80},
        {"name": "Woolworths Dishwashing Liquid 1L",            "brand": "Woolworths",     "size": "1L",    "base_price": 2.20},
        {"name": "Coles Smart Buy Dishwasher Tabs 40pk",        "brand": "Coles",          "size": "40pk",  "base_price": 7.00},
    ],

    # ── CLEANING ─────────────────────────────────────────────────────────────
    "cleaning": [
        {"name": "Glen 20 Spray N' Go Disinfectant 300g",       "brand": "Glen 20",        "size": "300g",  "base_price": 8.00},
        {"name": "Domestos Thick Bleach 750mL",                 "brand": "Domestos",       "size": "750mL", "base_price": 4.50},
        {"name": "Pine O Cleen Antibacterial 500mL",            "brand": "Pine O Cleen",   "size": "500mL", "base_price": 5.00},
        {"name": "Mr Muscle Kitchen Cleaner 500mL",             "brand": "Mr Muscle",      "size": "500mL", "base_price": 5.50},
        {"name": "Ajax Spray N' Wipe All Purpose 500mL",        "brand": "Ajax",           "size": "500mL", "base_price": 5.00},
        {"name": "Spray N Wipe Anti-Bacterial 500mL",           "brand": "Windex",         "size": "500mL", "base_price": 4.80},
        {"name": "Chux Multi-Purpose Wipes 60pk",               "brand": "Chux",           "size": "60pk",  "base_price": 6.00},
        {"name": "Woolworths Antibacterial Spray 750mL",        "brand": "Woolworths",     "size": "750mL", "base_price": 2.50},
    ],

    # ── MILK & DAIRY ─────────────────────────────────────────────────────────
    "milk": [
        {"name": "Devondale Full Cream Milk 1L",                "brand": "Devondale",      "size": "1L",    "base_price": 1.85},
        {"name": "A2 Full Cream Milk 2L",                       "brand": "A2",             "size": "2L",    "base_price": 5.90},
        {"name": "Dairy Road Full Cream Milk 2L",               "brand": "Dairy Road",     "size": "2L",    "base_price": 3.10},
        {"name": "Woolworths Full Cream Milk 3L",               "brand": "Woolworths",     "size": "3L",    "base_price": 4.50},
        {"name": "Pauls Full Cream Milk 2L",                    "brand": "Pauls",          "size": "2L",    "base_price": 3.80},
        {"name": "Oat Dream Oat Milk 1L",                       "brand": "Oat Dream",      "size": "1L",    "base_price": 4.20},
        {"name": "Almond Breeze Original 1L",                   "brand": "Blue Diamond",   "size": "1L",    "base_price": 4.00},
    ],

    # ── CHEESE ───────────────────────────────────────────────────────────────
    "cheese": [
        {"name": "Mainland Tasty Cheese Block 500g",            "brand": "Mainland",       "size": "500g",  "base_price": 9.50},
        {"name": "Bega Stringers Cheese 12pk",                  "brand": "Bega",           "size": "12pk",  "base_price": 5.50},
        {"name": "Perfect Italiano Parmesan 250g",              "brand": "Perfect Italiano","size": "250g",  "base_price": 6.00},
        {"name": "Woolworths Tasty Cheese Slices 500g",         "brand": "Woolworths",     "size": "500g",  "base_price": 6.50},
        {"name": "Coles Colby Cheese Block 500g",               "brand": "Coles",          "size": "500g",  "base_price": 7.00},
        {"name": "ALDI Emporium Selection Brie 125g",           "brand": "Emporium (ALDI)","size": "125g",  "base_price": 3.99},
    ],

    # ── BUTTER ───────────────────────────────────────────────────────────────
    "butter": [
        {"name": "Western Star Butter 500g",                    "brand": "Western Star",   "size": "500g",  "base_price": 8.20},
        {"name": "Devondale Butter Salted 500g",                "brand": "Devondale",      "size": "500g",  "base_price": 7.80},
        {"name": "Lurpak Spreadable Butter 250g",               "brand": "Lurpak",         "size": "250g",  "base_price": 6.50},
        {"name": "Woolworths Salted Butter 250g",               "brand": "Woolworths",     "size": "250g",  "base_price": 3.60},
    ],

    # ── BREAD ────────────────────────────────────────────────────────────────
    "bread": [
        {"name": "Wonder White Sliced Bread 700g",              "brand": "Wonder White",   "size": "700g",  "base_price": 4.20},
        {"name": "Helga's Traditional Rye 850g",                "brand": "Helga's",        "size": "850g",  "base_price": 4.90},
        {"name": "Abbott's Bakery Sourdough 680g",              "brand": "Abbott's Bakery","size": "680g",  "base_price": 5.20},
        {"name": "Woolworths White Sandwich Bread 650g",        "brand": "Woolworths",     "size": "650g",  "base_price": 2.40},
        {"name": "Tip Top Sunblest Multigrain 750g",            "brand": "Tip Top",        "size": "750g",  "base_price": 4.50},
        {"name": "Burgen Soy-Lin Bread 700g",                   "brand": "Burgen",         "size": "700g",  "base_price": 5.00},
    ],

    # ── EGGS ─────────────────────────────────────────────────────────────────
    "eggs": [
        {"name": "Sunny Queen Free Range Eggs 12pk",            "brand": "Sunny Queen",    "size": "12pk",  "base_price": 5.80},
        {"name": "Manning Valley Free Range Eggs 12pk",         "brand": "Manning Valley", "size": "12pk",  "base_price": 6.90},
        {"name": "Woolworths Cage Free Eggs 12pk",              "brand": "Woolworths",     "size": "12pk",  "base_price": 4.20},
        {"name": "Pace Farm Free Range Eggs 12pk",              "brand": "Pace Farm",      "size": "12pk",  "base_price": 6.00},
    ],

    # ── CHIPS / SNACKS ───────────────────────────────────────────────────────
    "chips": [
        {"name": "Smith's Original Potato Chips 170g",          "brand": "Smith's",        "size": "170g",  "base_price": 4.80},
        {"name": "Red Rock Deli Sea Salt 165g",                 "brand": "Red Rock Deli",  "size": "165g",  "base_price": 6.30},
        {"name": "Pringles Original 134g",                      "brand": "Pringles",       "size": "134g",  "base_price": 5.00},
        {"name": "Kettle Sea Salt Potato Chips 175g",           "brand": "Kettle",         "size": "175g",  "base_price": 5.50},
        {"name": "Doritos Cheese Supreme 170g",                 "brand": "Doritos",        "size": "170g",  "base_price": 4.50},
        {"name": "Thins Original Potato Chips 175g",            "brand": "Thins",          "size": "175g",  "base_price": 4.20},
        {"name": "Woolworths BBQ Chips 200g",                   "brand": "Woolworths",     "size": "200g",  "base_price": 2.50},
    ],

    # ── CHOCOLATE ────────────────────────────────────────────────────────────
    "chocolate": [
        {"name": "Cadbury Dairy Milk Chocolate 180g",           "brand": "Cadbury",        "size": "180g",  "base_price": 8.00},
        {"name": "Lindt Excellence Dark 70% 100g",              "brand": "Lindt",          "size": "100g",  "base_price": 6.00},
        {"name": "Kit Kat Original 45g",                        "brand": "Nestlé",         "size": "45g",   "base_price": 2.20},
        {"name": "Twix Chocolate Bar 50g",                      "brand": "Mars",           "size": "50g",   "base_price": 2.50},
        {"name": "Allen's Party Mix Lollies 200g",              "brand": "Allen's",        "size": "200g",  "base_price": 4.00},
        {"name": "Freddo Faces Chocolate 72g",                  "brand": "Cadbury",        "size": "72g",   "base_price": 3.50},
        {"name": "Woolworths Dark Chocolate 200g",              "brand": "Woolworths",     "size": "200g",  "base_price": 3.00},
    ],

    # ── COFFEE ───────────────────────────────────────────────────────────────
    "coffee": [
        {"name": "Moccona Classic Medium Roast 400g",           "brand": "Moccona",        "size": "400g",  "base_price": 28.00},
        {"name": "Nescafe Blend 43 Instant Coffee 500g",        "brand": "Nescafe",        "size": "500g",  "base_price": 22.00},
        {"name": "Vittoria Mountain Blend Coffee Beans 1kg",    "brand": "Vittoria",       "size": "1kg",   "base_price": 36.00},
        {"name": "Lavazza Crema e Gusto Espresso 1kg",          "brand": "Lavazza",        "size": "1kg",   "base_price": 34.00},
        {"name": "Woolworths Instant Coffee 150g",              "brand": "Woolworths",     "size": "150g",  "base_price": 5.50},
        {"name": "ALDI Lazzio Coffee Capsules 10pk",            "brand": "Lazzio (ALDI)",  "size": "10pk",  "base_price": 3.99},
    ],

    # ── SOFT DRINKS ──────────────────────────────────────────────────────────
    "cola": [
        {"name": "Coca-Cola Classic 30x375mL Cans",             "brand": "Coca-Cola",      "size": "30pk",  "base_price": 38.00},
        {"name": "Coca-Cola Zero Sugar 2L Bottle",              "brand": "Coca-Cola",      "size": "2L",    "base_price": 4.50},
        {"name": "Pepsi Max 1.25L",                             "brand": "Pepsi",          "size": "1.25L", "base_price": 3.50},
        {"name": "Woolworths Cola 2L",                          "brand": "Woolworths",     "size": "2L",    "base_price": 2.00},
    ],

    # ── NAPPIES / BABY ───────────────────────────────────────────────────────
    "nappy": [
        {"name": "Huggies Ultimate Nappies Size 3 56pk",        "brand": "Huggies",        "size": "56pk",  "base_price": 32.00},
        {"name": "Babylove Cosifit Nappies Size 3 50pk",        "brand": "Babylove",       "size": "50pk",  "base_price": 24.00},
        {"name": "Woolworths Little Ones Nappies 50pk",         "brand": "Woolworths",     "size": "50pk",  "base_price": 11.50},
        {"name": "Pampers Baby Dry Nappies Size 3 52pk",        "brand": "Pampers",        "size": "52pk",  "base_price": 28.00},
    ],

    # ── SHAMPOO / HAIR ───────────────────────────────────────────────────────
    "shampoo": [
        {"name": "Head & Shoulders Classic Clean 660mL",        "brand": "Head & Shoulders","size": "660mL", "base_price": 10.00},
        {"name": "Pantene Smooth & Sleek Shampoo 700mL",        "brand": "Pantene",        "size": "700mL", "base_price": 9.50},
        {"name": "Dove Nourishing Moisture Shampoo 700mL",      "brand": "Dove",           "size": "700mL", "base_price": 9.00},
        {"name": "Elvive Dream Lengths Shampoo 400mL",          "brand": "L'Oréal",        "size": "400mL", "base_price": 7.50},
        {"name": "Woolworths Moisturising Shampoo 400mL",       "brand": "Woolworths",     "size": "400mL", "base_price": 2.50},
        {"name": "ALDI Lacura Argan Oil Shampoo 400mL",         "brand": "Lacura (ALDI)",  "size": "400mL", "base_price": 2.99},
    ],

    # ── DEODORANT ────────────────────────────────────────────────────────────
    "deodorant": [
        {"name": "Rexona Men Active Dry 250mL",                 "brand": "Rexona",         "size": "250mL", "base_price": 6.50},
        {"name": "Dove Original Anti-Perspirant 250mL",         "brand": "Dove",           "size": "250mL", "base_price": 6.00},
        {"name": "Lynx Africa Deodorant Body Spray 165mL",      "brand": "Lynx",           "size": "165mL", "base_price": 5.50},
        {"name": "Sure Women Cotton Dry 250mL",                 "brand": "Sure",           "size": "250mL", "base_price": 5.50},
        {"name": "Woolworths Deodorant Spray 150mL",            "brand": "Woolworths",     "size": "150mL", "base_price": 2.00},
    ],

    # ── TOOTHPASTE ───────────────────────────────────────────────────────────
    "toothpaste": [
        {"name": "Colgate Triple Action Toothpaste 200g",       "brand": "Colgate",        "size": "200g",  "base_price": 4.80},
        {"name": "Oral-B Pro-Health Toothpaste 200g",           "brand": "Oral-B",         "size": "200g",  "base_price": 5.50},
        {"name": "Sensodyne Rapid Relief Toothpaste 110g",      "brand": "Sensodyne",      "size": "110g",  "base_price": 7.00},
        {"name": "Arm & Hammer Baking Soda Toothpaste 125g",    "brand": "Arm & Hammer",   "size": "125g",  "base_price": 5.00},
        {"name": "Woolworths Whitening Toothpaste 175g",        "brand": "Woolworths",     "size": "175g",  "base_price": 2.00},
    ],

    # ── BREAKFAST CEREAL ─────────────────────────────────────────────────────
    "cereal": [
        {"name": "Kellogg's Corn Flakes 725g",                  "brand": "Kellogg's",      "size": "725g",  "base_price": 5.50},
        {"name": "Sanitarium Weet-Bix 750g",                    "brand": "Sanitarium",     "size": "750g",  "base_price": 5.00},
        {"name": "Uncle Tobys Rolled Oats 1kg",                 "brand": "Uncle Tobys",    "size": "1kg",   "base_price": 5.50},
        {"name": "Kellogg's Special K Original 500g",           "brand": "Kellogg's",      "size": "500g",  "base_price": 7.00},
        {"name": "Woolworths Corn Flakes 500g",                 "brand": "Woolworths",     "size": "500g",  "base_price": 2.50},
        {"name": "ALDI Harvest Morn Muesli 1kg",                "brand": "Harvest Morn (ALDI)","size": "1kg","base_price": 3.49},
    ],

    # ── PASTA ────────────────────────────────────────────────────────────────
    "pasta": [
        {"name": "San Remo Penne Rigati 500g",                  "brand": "San Remo",       "size": "500g",  "base_price": 2.20},
        {"name": "Barilla Spaghetti No. 5 500g",                "brand": "Barilla",        "size": "500g",  "base_price": 2.80},
        {"name": "Latina Fresh Fettuccine 625g",                "brand": "Latina Fresh",   "size": "625g",  "base_price": 5.50},
        {"name": "Woolworths Pasta Spirals 500g",               "brand": "Woolworths",     "size": "500g",  "base_price": 1.10},
    ],

    # ── RICE ─────────────────────────────────────────────────────────────────
    "rice": [
        {"name": "SunRice Long Grain White Rice 5kg",           "brand": "SunRice",        "size": "5kg",   "base_price": 12.00},
        {"name": "Sunrice Medium Grain 5kg",                    "brand": "SunRice",        "size": "5kg",   "base_price": 11.50},
        {"name": "Woolworths Long Grain Rice 5kg",              "brand": "Woolworths",     "size": "5kg",   "base_price": 7.50},
        {"name": "Ben's Original Long Grain Rice 750g",         "brand": "Ben's Original", "size": "750g",  "base_price": 3.50},
    ],

    # ── YOGHURT ──────────────────────────────────────────────────────────────
    "yoghurt": [
        {"name": "Chobani Natural Yoghurt 907g",                "brand": "Chobani",        "size": "907g",  "base_price": 9.00},
        {"name": "Jalna Greek Yoghurt 500g",                    "brand": "Jalna",          "size": "500g",  "base_price": 6.50},
        {"name": "Danone YoPRO Vanilla 160g",                   "brand": "Danone",         "size": "160g",  "base_price": 2.80},
        {"name": "Woolworths Greek Style Yoghurt 1kg",          "brand": "Woolworths",     "size": "1kg",   "base_price": 4.50},
        {"name": "ALDI Brooklea Greek Yoghurt 1kg",             "brand": "Brooklea (ALDI)","size": "1kg",   "base_price": 3.49},
    ],

    # ── JUICE ────────────────────────────────────────────────────────────────
    "juice": [
        {"name": "Tropicana Pure Orange Juice 1L",              "brand": "Tropicana",      "size": "1L",    "base_price": 5.50},
        {"name": "Golden Circle Orange Juice 1L",               "brand": "Golden Circle",  "size": "1L",    "base_price": 4.00},
        {"name": "Nudie Nothing But Juice Orange 1L",           "brand": "Nudie",          "size": "1L",    "base_price": 6.50},
        {"name": "Woolworths Fresh OJ 1L",                      "brand": "Woolworths",     "size": "1L",    "base_price": 3.00},
    ],

    # ── WATER ────────────────────────────────────────────────────────────────
    "water": [
        {"name": "Mount Franklin Sparkling Water 1.25L",        "brand": "Mount Franklin", "size": "1.25L", "base_price": 3.00},
        {"name": "Evian Natural Spring Water 1.5L",             "brand": "Evian",          "size": "1.5L",  "base_price": 4.50},
        {"name": "Woolworths Spring Water 10x600mL",            "brand": "Woolworths",     "size": "10pk",  "base_price": 4.00},
        {"name": "ALDI Just Water 6x1.5L",                      "brand": "ALDI",           "size": "6pk",   "base_price": 3.49},
    ],

    # ── TISSUES & PAPER ──────────────────────────────────────────────────────
    "tissues": [
        {"name": "Kleenex Thick Care Tissues 3ply 200pk",       "brand": "Kleenex",        "size": "200pk", "base_price": 6.50},
        {"name": "Sorbent White Tissues 224pk",                 "brand": "Sorbent",        "size": "224pk", "base_price": 5.50},
        {"name": "Woolworths Mansize Tissues 100pk",            "brand": "Woolworths",     "size": "100pk", "base_price": 2.00},
    ],

    # ── TOILET PAPER ─────────────────────────────────────────────────────────
    "toilet": [
        {"name": "Quilton Double Length 3-Ply 24pk",            "brand": "Quilton",        "size": "24pk",  "base_price": 18.00},
        {"name": "Sorbent Silky White Toilet Tissue 24pk",      "brand": "Sorbent",        "size": "24pk",  "base_price": 16.00},
        {"name": "ALDI Confidence Toilet Tissue 24pk",          "brand": "Confidence (ALDI)","size": "24pk","base_price": 8.99},
        {"name": "Woolworths Toilet Tissue 36pk",               "brand": "Woolworths",     "size": "36pk",  "base_price": 14.00},
        {"name": "Coles Ultra White Toilet Tissue 24pk",        "brand": "Coles",          "size": "24pk",  "base_price": 13.00},
    ],

    # ── SUNSCREEN / PERSONAL CARE ────────────────────────────────────────────
    "sunscreen": [
        {"name": "Cancer Council SPF 50+ Sunscreen 200mL",      "brand": "Cancer Council", "size": "200mL", "base_price": 12.00},
        {"name": "Banana Boat Ultra Sport SPF 50+ 175mL",       "brand": "Banana Boat",    "size": "175mL", "base_price": 14.00},
        {"name": "Woolworths SPF 50+ Sunscreen 200mL",          "brand": "Woolworths",     "size": "200mL", "base_price": 5.50},
    ],

    # ── VITAMINS / HEALTH ────────────────────────────────────────────────────
    "vitamins": [
        {"name": "Blackmores Vitamin C 500mg 120 tablets",      "brand": "Blackmores",     "size": "120 tab","base_price": 18.00},
        {"name": "Centrum Adults Multivitamin 200 tablets",     "brand": "Centrum",        "size": "200 tab","base_price": 22.00},
        {"name": "Swisse Ultiboost Magnesium 200 tablets",      "brand": "Swisse",         "size": "200 tab","base_price": 24.00},
        {"name": "Woolworths Vitamin D 1000IU 100 capsules",    "brand": "Woolworths",     "size": "100 cap","base_price": 6.50},
    ],

    # ── PET FOOD ─────────────────────────────────────────────────────────────
    "pet": [
        {"name": "Purina Pro Plan Adult Dry Dog Food 3kg",      "brand": "Purina",         "size": "3kg",   "base_price": 28.00},
        {"name": "Whiskas Chicken Wet Cat Food 12x85g",         "brand": "Whiskas",        "size": "12pk",  "base_price": 12.00},
        {"name": "Pedigree Adult Dry Dog Food 10kg",            "brand": "Pedigree",       "size": "10kg",  "base_price": 36.00},
        {"name": "Woolworths Cat Food Tuna Variety 12pk",       "brand": "Woolworths",     "size": "12pk",  "base_price": 6.50},
    ],

    # ── FROZEN MEALS ─────────────────────────────────────────────────────────
    "frozen": [
        {"name": "McCain Superfries Classic 1kg",               "brand": "McCain",         "size": "1kg",   "base_price": 5.50},
        {"name": "Birds Eye Crispy Chicken Nuggets 700g",       "brand": "Birds Eye",      "size": "700g",  "base_price": 10.00},
        {"name": "San Remo Creamy Pasta Bake 1kg",              "brand": "San Remo",       "size": "1kg",   "base_price": 7.50},
        {"name": "Woolworths Frozen Peas 1kg",                  "brand": "Woolworths",     "size": "1kg",   "base_price": 2.50},
        {"name": "ALDI Frozen Beef Lasagne 400g",               "brand": "ALDI",           "size": "400g",  "base_price": 3.99},
    ],

    # ── ICE CREAM ────────────────────────────────────────────────────────────
    "ice cream": [
        {"name": "Streets Blue Ribbon Ice Cream 2L",            "brand": "Streets",        "size": "2L",    "base_price": 11.00},
        {"name": "Ben & Jerry's Choc Chip Cookie Dough 458mL",  "brand": "Ben & Jerry's",  "size": "458mL", "base_price": 12.00},
        {"name": "Connoisseur Vanilla Bean Ice Cream 4pk",      "brand": "Connoisseur",    "size": "4pk",   "base_price": 8.00},
        {"name": "Woolworths Vanilla Ice Cream 2L",             "brand": "Woolworths",     "size": "2L",    "base_price": 5.00},
        {"name": "ALDI Moser Roth Ice Cream Bar 4pk",           "brand": "Moser Roth (ALDI)","size":"4pk",  "base_price": 4.99},
    ],

    # ── COOKING OIL ──────────────────────────────────────────────────────────
    "oil": [
        {"name": "Bertolli Extra Virgin Olive Oil 750mL",       "brand": "Bertolli",       "size": "750mL", "base_price": 12.00},
        {"name": "Cobram Estate EVOO 500mL",                    "brand": "Cobram Estate",  "size": "500mL", "base_price": 10.00},
        {"name": "Woolworths Canola Oil 1L",                    "brand": "Woolworths",     "size": "1L",    "base_price": 3.50},
        {"name": "Celebrate Health Coconut Oil 300mL",          "brand": "Celebrate Health","size": "300mL","base_price": 8.00},
    ],

    # ── CANNED GOODS ─────────────────────────────────────────────────────────
    "canned": [
        {"name": "SPC Diced Tomatoes 400g",                     "brand": "SPC",            "size": "400g",  "base_price": 1.80},
        {"name": "John West Tuna in Spring Water 425g",         "brand": "John West",      "size": "425g",  "base_price": 4.00},
        {"name": "Edgell Chickpeas 400g",                       "brand": "Edgell",         "size": "400g",  "base_price": 1.50},
        {"name": "Woolworths Diced Tomatoes 4pk",               "brand": "Woolworths",     "size": "4pk",   "base_price": 3.50},
    ],

    # ── CONDIMENTS / SAUCE ───────────────────────────────────────────────────
    "sauce": [
        {"name": "Leggo's Tomato Pasta Sauce Classic 700g",     "brand": "Leggo's",        "size": "700g",  "base_price": 3.50},
        {"name": "Dolmio Bolognese Pasta Sauce 500g",           "brand": "Dolmio",         "size": "500g",  "base_price": 3.80},
        {"name": "Fountain Tomato Sauce 500mL",                 "brand": "Fountain",       "size": "500mL", "base_price": 2.80},
        {"name": "Masterfoods BBQ Sauce 550mL",                 "brand": "Masterfoods",    "size": "550mL", "base_price": 4.00},
        {"name": "Woolworths Tomato Sauce 500mL",               "brand": "Woolworths",     "size": "500mL", "base_price": 1.80},
    ],

    # ── COKE / SOFT DRINK (alias) ────────────────────────────────────────────
    "coke": [
        {"name": "Coca-Cola Classic 30x375mL Cans",             "brand": "Coca-Cola",      "size": "30pk",  "base_price": 38.00},
        {"name": "Coca-Cola Zero Sugar 2L Bottle",              "brand": "Coca-Cola",      "size": "2L",    "base_price": 4.50},
        {"name": "Diet Coke 10x375mL Cans",                     "brand": "Coca-Cola",      "size": "10pk",  "base_price": 14.00},
        {"name": "Woolworths Cola 2L",                          "brand": "Woolworths",     "size": "2L",    "base_price": 2.00},
    ],

    # ── MEAT / CHICKEN ───────────────────────────────────────────────────────
    "chicken": [
        {"name": "Steggles Chicken Breast Fillets 1kg",         "brand": "Steggles",       "size": "1kg",   "base_price": 14.00},
        {"name": "Lilydale Free Range Chicken Thighs 1kg",      "brand": "Lilydale",       "size": "1kg",   "base_price": 12.00},
        {"name": "Woolworths RSPCA Chicken Mince 500g",         "brand": "Woolworths",     "size": "500g",  "base_price": 6.50},
        {"name": "Ingham's Chicken Nuggets 750g",               "brand": "Ingham's",       "size": "750g",  "base_price": 9.50},
    ],

    "beef": [
        {"name": "Woolworths Beef Mince Regular 500g",          "brand": "Woolworths",     "size": "500g",  "base_price": 7.50},
        {"name": "Coles Beef Sausages Thick 600g",              "brand": "Coles",          "size": "600g",  "base_price": 7.00},
        {"name": "Don Beef Pastrami 100g",                      "brand": "Don",            "size": "100g",  "base_price": 5.50},
        {"name": "Primo Beef Burger Patties 4pk",               "brand": "Primo",          "size": "4pk",   "base_price": 8.00},
    ],

    # ── FISH / SEAFOOD ───────────────────────────────────────────────────────
    "fish": [
        {"name": "John West Salmon in Spring Water 415g",       "brand": "John West",      "size": "415g",  "base_price": 5.50},
        {"name": "Woolworths Barramundi Fillets 500g",          "brand": "Woolworths",     "size": "500g",  "base_price": 11.00},
        {"name": "Young's Battered Cod 400g",                   "brand": "Young's",        "size": "400g",  "base_price": 8.50},
    ],

    # ── BABY FORMULA ─────────────────────────────────────────────────────────
    "formula": [
        {"name": "Aptamil Gold+ Stage 1 Infant Formula 900g",   "brand": "Aptamil",        "size": "900g",  "base_price": 35.00},
        {"name": "NAN Optipro Stage 1 Infant Formula 800g",     "brand": "NAN",            "size": "800g",  "base_price": 30.00},
        {"name": "S-26 Gold Newborn Stage 1 800g",              "brand": "S-26",           "size": "800g",  "base_price": 32.00},
        {"name": "Bellamy's Organic Infant Formula 800g",       "brand": "Bellamy's",      "size": "800g",  "base_price": 38.00},
    ],

    # ── BEER & WINE (as grocery items) ───────────────────────────────────────
    "beer": [
        {"name": "Victoria Bitter VB 30x375mL Cans",            "brand": "VB",             "size": "30pk",  "base_price": 60.00},
        {"name": "Carlton Draught 24x375mL Cans",               "brand": "Carlton",        "size": "24pk",  "base_price": 52.00},
        {"name": "Cascade Premium Light 24pk",                  "brand": "Cascade",        "size": "24pk",  "base_price": 44.00},
        {"name": "James Squire One Fifty Lashes 6pk",           "brand": "James Squire",   "size": "6pk",   "base_price": 22.00},
        {"name": "ALDI Moose Head 6pk",                         "brand": "ALDI",           "size": "6pk",   "base_price": 9.99},
    ],

    # ── PAPER TOWEL ──────────────────────────────────────────────────────────
    "paper towel": [
        {"name": "Viva White Paper Towel 3pk",                  "brand": "Viva",           "size": "3pk",   "base_price": 6.00},
        {"name": "Sorbent Paper Towel White 4pk",               "brand": "Sorbent",        "size": "4pk",   "base_price": 5.00},
        {"name": "Woolworths Paper Towel 4pk",                  "brand": "Woolworths",     "size": "4pk",   "base_price": 3.50},
        {"name": "ALDI Confidence Paper Towel 4pk",             "brand": "Confidence (ALDI)","size": "4pk", "base_price": 2.49},
    ],

    # ── VEGEMITE / SPREADS ───────────────────────────────────────────────────
    "vegemite": [
        {"name": "Vegemite Original Spread 380g",               "brand": "Vegemite",       "size": "380g",  "base_price": 6.00},
        {"name": "Bega Smooth Peanut Butter 470g",              "brand": "Bega",           "size": "470g",  "base_price": 5.00},
        {"name": "Nutella Hazelnut Spread 750g",                "brand": "Nutella",        "size": "750g",  "base_price": 8.50},
        {"name": "Woolworths Strawberry Jam 500g",              "brand": "Woolworths",     "size": "500g",  "base_price": 2.50},
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# KEYWORD ALIASES  (maps common search words → catalog keys)
# ──────────────────────────────────────────────────────────────────────────────
ALIASES = {
    # laundry synonyms
    "laundry":      "laundry",
    "washing":      "laundry",
    "detergent":    "laundry",
    "washing powder":"laundry",
    "washing liquid":"laundry",
    "dynamo":       "laundry",
    "omo":          "laundry",
    "cold power":   "laundry",
    "biozet":       "laundry",
    "radiant":      "laundry",
    "surf":         "laundry",
    "fab":          "laundry",
    "persil":       "laundry",
    "napisan":      "laundry",
    # dish
    "dish":         "dishwashing",
    "dishwashing":  "dishwashing",
    "finish":       "dishwashing",
    "fairy":        "dishwashing",
    "morning fresh":"dishwashing",
    # clean
    "clean":        "cleaning",
    "bleach":       "cleaning",
    "disinfectant": "cleaning",
    "spray":        "cleaning",
    "domestos":     "cleaning",
    "pine o cleen": "cleaning",
    "glen 20":      "cleaning",
    # dairy
    "milk":         "milk",
    "oat milk":     "milk",
    "almond milk":  "milk",
    "cheese":       "cheese",
    "butter":       "butter",
    "yoghurt":      "yoghurt",
    "yogurt":       "yoghurt",
    # bread/baked
    "bread":        "bread",
    "toast":        "bread",
    # eggs
    "eggs":         "eggs",
    "egg":          "eggs",
    # chips/snacks
    "chips":        "chips",
    "crisps":       "chips",
    "smiths":       "chips",
    "pringles":     "chips",
    "kettle":       "chips",
    "doritos":      "chips",
    "snacks":       "chips",
    # chocolate/sweets
    "chocolate":    "chocolate",
    "cadbury":      "chocolate",
    "lolly":        "chocolate",
    "lollies":      "chocolate",
    "candy":        "chocolate",
    "sweets":       "chocolate",
    # coffee
    "coffee":       "coffee",
    "moccona":      "coffee",
    "nescafe":      "coffee",
    "vittoria":     "coffee",
    # drinks
    "coke":         "coke",
    "cola":         "cola",
    "soft drink":   "coke",
    "soda":         "coke",
    "pepsi":        "cola",
    "juice":        "juice",
    "orange juice": "juice",
    "water":        "water",
    "sparkling":    "water",
    "beer":         "beer",
    "ale":          "beer",
    "lager":        "beer",
    # cereal
    "cereal":       "cereal",
    "weet-bix":     "cereal",
    "weetbix":      "cereal",
    "oats":         "cereal",
    "muesli":       "cereal",
    "corn flakes":  "cereal",
    # pasta / rice
    "pasta":        "pasta",
    "spaghetti":    "pasta",
    "penne":        "pasta",
    "rice":         "rice",
    # nappies / baby
    "nappy":        "nappy",
    "nappies":      "nappy",
    "huggies":      "nappy",
    "pampers":      "nappy",
    "baby":         "nappy",
    "babylove":     "nappy",
    "formula":      "formula",
    "infant formula":"formula",
    # health / personal
    "shampoo":      "shampoo",
    "conditioner":  "shampoo",
    "hair":         "shampoo",
    "deodorant":    "deodorant",
    "deo":          "deodorant",
    "toothpaste":   "toothpaste",
    "teeth":        "toothpaste",
    "dental":       "toothpaste",
    "sunscreen":    "sunscreen",
    "sunblock":     "sunscreen",
    "spf":          "sunscreen",
    "vitamins":     "vitamins",
    "vitamin":      "vitamins",
    "supplement":   "vitamins",
    # paper goods
    "tissues":      "tissues",
    "tissue":       "tissues",
    "kleenex":      "tissues",
    "toilet paper": "toilet",
    "toilet tissue":"toilet",
    "loo":          "toilet",
    "quilton":      "toilet",
    "paper towel":  "paper towel",
    "paper towels": "paper towel",
    # cooking
    "oil":          "oil",
    "olive oil":    "oil",
    "canola":       "oil",
    "sauce":        "sauce",
    "pasta sauce":  "sauce",
    "tomato sauce": "sauce",
    "bbq sauce":    "sauce",
    "canned":       "canned",
    "cans":         "canned",
    "tuna":         "canned",
    "tomato":       "canned",
    # meat
    "chicken":      "chicken",
    "beef":         "beef",
    "steak":        "beef",
    "mince":        "beef",
    "sausage":      "beef",
    "fish":         "fish",
    "seafood":      "fish",
    "salmon":       "fish",
    # frozen
    "frozen":       "frozen",
    "nuggets":      "frozen",
    "chips frozen": "frozen",
    "ice cream":    "ice cream",
    "icecream":     "ice cream",
    "gelato":       "ice cream",
    # pet
    "pet":          "pet",
    "dog":          "pet",
    "cat":          "pet",
    "dog food":     "pet",
    "cat food":     "pet",
    "purina":       "pet",
    # spreads
    "vegemite":     "vegemite",
    "peanut butter":"vegemite",
    "jam":          "vegemite",
    "nutella":      "vegemite",
    "spread":       "vegemite",
}


def resolve_catalog_key(query: str):
    """Return matching catalog key(s) for a query string."""
    q = query.lower().strip()

    # 1. Exact alias match
    if q in ALIASES:
        return ALIASES[q]

    # 2. Exact catalog key match
    if q in CATALOG:
        return q

    # 3. Partial alias match (query is substring of an alias key, or vice versa)
    best = None
    for alias_key, cat_key in ALIASES.items():
        if alias_key in q or q in alias_key:
            best = cat_key
            break

    if best:
        return best

    # 4. Partial catalog key match
    for cat_key in CATALOG:
        if cat_key in q or q in cat_key:
            return cat_key

    # 5. Scan catalog product names for a brand/keyword match
    q_words = set(q.split())
    for cat_key, products in CATALOG.items():
        for product in products:
            name_lower = product["name"].lower()
            brand_lower = product["brand"].lower()
            if q in name_lower or q in brand_lower:
                return cat_key
            # word overlap
            name_words = set(name_lower.split())
            if len(q_words & name_words) >= 1 and len(q_words) >= 2:
                return cat_key

    return None


def get_store_availability(brand_name, product_name):
    brand_lower = brand_name.lower()
    name_lower = product_name.lower()
    
    # Woolworths private label
    if "woolworths" in brand_lower or "woolworths" in name_lower or "everyday" in brand_lower:
        return ["Woolworths"]
        
    # Coles private label
    if "coles" in brand_lower or "coles" in name_lower or "smart buy" in name_lower:
        return ["Coles"]
        
    # ALDI private label / exclusive brands
    aldi_brands = ["aldi", "almat", "emporium", "lazzio", "lacura", "harvest morn", "moser roth", "confidence", "dairy road", "moose head"]
    if any(ab in brand_lower or ab in name_lower for ab in aldi_brands):
        return ["ALDI"]
        
    # Standard name brands are available at Woolworths and Coles (not ALDI)
    return ["Woolworths", "Coles"]


def make_result(template, query, idx, category=None):
    base = template["base_price"]
    brand = template["brand"]
    name = template["name"]

    # Determine availability
    avail = get_store_availability(brand, name)

    woolies_price = base
    coles_price = round(base * random.choice([0.94, 0.97, 1.0, 1.03, 1.06]), 2)
    aldi_price = round(base * random.choice([0.80, 0.83, 0.86, 0.89]), 2)

    # Filter to available prices to calculate min_price
    prices = []
    if "Woolworths" in avail:
        prices.append(woolies_price)
    if "Coles" in avail:
        prices.append(coles_price)
    if "ALDI" in avail:
        prices.append(aldi_price)

    min_price = min(prices) if prices else base

    badge = ""
    woolies_orig = None
    coles_orig = None

    promo = random.choice(["woolies_special", "coles_special", "none", "none"])
    is_home_brand = brand.lower() in ("woolworths", "coles", "aldi")

    if promo == "woolies_special" and "Woolworths" in avail and not is_home_brand:
        woolies_price = round(base * 0.50, 2)
        woolies_orig = base
        badge = "Half Price @ Woolies"
        min_price = min(woolies_price, coles_price) if "Coles" in avail else woolies_price
    elif promo == "coles_special" and "Coles" in avail and not is_home_brand:
        coles_price = round(base * 0.50, 2)
        coles_orig = base
        badge = "Half Price @ Coles"
        min_price = min(woolies_price, coles_price) if "Woolworths" in avail else coles_price
    else:
        if "ALDI" in avail:
            badge = "ALDI Best Deal" if aldi_price == min_price else ("Woolies Special" if woolies_price == min_price else "Coles Special")
        else:
            badge = "Woolies Special" if woolies_price == min_price else "Coles Special"

    stores = [
        {
            "name": "Woolworths",
            "price": woolies_price if "Woolworths" in avail else None,
            "original": woolies_orig if "Woolworths" in avail else None,
            "isBest": "Woolworths" in avail and woolies_price == min_price,
            "logo": "W",
            "logoClass": "bg-woolies"
        },
        {
            "name": "Coles",
            "price": coles_price if "Coles" in avail else None,
            "original": coles_orig if "Coles" in avail else None,
            "isBest": "Coles" in avail and coles_price == min_price,
            "logo": "C",
            "logoClass": "bg-coles"
        },
        {
            "name": "ALDI",
            "price": aldi_price if "ALDI" in avail else None,
            "original": None,
            "isBest": "ALDI" in avail and aldi_price == min_price,
            "logo": "A",
            "logoClass": "bg-aldi"
        }
    ]

    return {
        "id": f"scraped_{query.replace(' ', '_')}_{idx}",
        "name": name,
        "brand": brand,
        "badge": badge,
        "category": category,
        "stores": stores
    }


# ──────────────────────────────────────────────────────────────────────────────
# FIREBASE FIRESTORE INTEGRATION & CATALOG CACHE
# ──────────────────────────────────────────────────────────────────────────────
db = None
FIRESTORE_CATALOG = {}
FIRESTORE_LAST_LOADED = 0

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    cred_path = os.path.join(DIRECTORY, 'firebase-credentials.json')
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'projectId': 'pantrybloom'
        }, name='server_app')
        db = firestore.client(app=firebase_admin.get_app('server_app'))
        print("Server successfully initialized Firebase Admin SDK (Project: pantrybloom).")
    else:
        print("Server warning: firebase-credentials.json not found. Firestore features disabled.")
except Exception as e:
    print("Server failed to initialize Firebase Admin SDK:", e)

def load_firestore_catalog():
    global FIRESTORE_CATALOG, FIRESTORE_LAST_LOADED
    if db is None:
        # Fallback to local scraped JSON if it exists
        fallback_path = os.path.join(DIRECTORY, 'scraped_products_fallback.json')
        if os.path.exists(fallback_path):
            try:
                with open(fallback_path, 'r', encoding='utf-8') as f:
                    fallback_data = json.load(f)
                
                new_catalog = {}
                for pid, pdata in fallback_data.items():
                    cat = pdata.get('category', 'general')
                    if cat not in new_catalog:
                        new_catalog[cat] = []
                    
                    new_catalog[cat].append({
                        "id": pid,
                        "name": pdata.get('name'),
                        "brand": pdata.get('brand'),
                        "size": pdata.get('size'),
                        "image_url": pdata.get('image_url'),
                        "barcode": pdata.get('barcode', ''),
                        "prices": pdata.get('prices', {})
                    })
                FIRESTORE_CATALOG = new_catalog
                FIRESTORE_LAST_LOADED = time.time()
                print(f"Loaded {sum(len(v) for v in FIRESTORE_CATALOG.values())} products from local scraped fallback JSON.")
            except Exception as e:
                print("Failed loading local scraped fallback JSON:", e)
        return

    try:
        print("Loading product catalog from Firebase Firestore (scraped_products)...")
        new_catalog = {}
        products_ref = db.collection('scraped_products')
        docs = products_ref.stream()
        
        count = 0
        for doc in docs:
            pdata = doc.to_dict()
            pid = doc.id
            cat = pdata.get('category', 'general')
            if cat not in new_catalog:
                new_catalog[cat] = []
                
            # Get the prices subcollection for this product
            prices = {}
            prices_ref = doc.reference.collection('prices').stream()
            for price_doc in prices_ref:
                prices[price_doc.id] = price_doc.to_dict()
                
            new_catalog[cat].append({
                "id": pid,
                "name": pdata.get('name'),
                "brand": pdata.get('brand'),
                "size": pdata.get('size'),
                "image_url": pdata.get('image_url'),
                "barcode": pdata.get('barcode', ''),
                "prices": prices
            })
            count += 1
            
        FIRESTORE_CATALOG = new_catalog
        FIRESTORE_LAST_LOADED = time.time()
        print(f"Successfully loaded {count} products from Firestore collection 'scraped_products'.")
    except Exception as e:
        print("Error loading catalog from Firestore:", e)

def make_firestore_result(product, query, idx, category=None):
    name = product["name"]
    brand = product["brand"]
    pid = product["id"]
    prices = product["prices"]
    
    valid_prices = [pdata["price"] for pdata in prices.values() if pdata.get("price") is not None]
    min_price = min(valid_prices) if valid_prices else 0.0
    
    badge = ""
    for store_name, pdata in prices.items():
        if pdata.get("is_promo") and pdata.get("promo_desc"):
            badge = f"{store_name} Special"
            desc = pdata.get("promo_desc").lower()
            if "half" in desc or "50%" in desc or (pdata.get("original_price") and round(pdata["price"]/pdata["original_price"], 2) == 0.5):
                badge = f"Half Price @ {store_name}"
            break
            
    if not badge:
        best_stores = [s for s, pd in prices.items() if pd.get("price") == min_price]
        if best_stores:
            badge = f"{best_stores[0]} Best Deal"
        else:
            badge = "Compare Price"
            
    stores = []
    for store_name, logo, logo_class in [("Woolworths", "W", "bg-woolies"), ("Coles", "C", "bg-coles"), ("ALDI", "A", "bg-aldi")]:
        pdata = prices.get(store_name)
        if pdata:
            price = pdata.get("price")
            orig = pdata.get("original_price")
            if orig == price:
                orig = None
            stores.append({
                "name": store_name,
                "price": price,
                "original": orig,
                "isBest": price == min_price and price is not None,
                "logo": logo,
                "logoClass": logo_class
            })
        else:
            stores.append({
                "name": store_name,
                "price": None,
                "original": None,
                "isBest": False,
                "logo": logo,
                "logoClass": logo_class
            })
            
    return {
        "id": pid,
        "name": name,
        "brand": brand,
        "badge": badge,
        "category": category if category else "general",
        "stores": stores
    }

def run_daily_scheduler():
    while True:
        try:
            now = datetime.datetime.now()
            target = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if target <= now:
                target += datetime.timedelta(days=1)
                
            sleep_seconds = (target - now).total_seconds()
            print(f"Daily Scraper Scheduler: Next scheduled crawl at {target.strftime('%Y-%m-%d %H:%M:%S')} (sleeping for {round(sleep_seconds/3600, 2)} hours)")
            
            while sleep_seconds > 0:
                time.sleep(min(60, sleep_seconds))
                sleep_seconds -= 60
                
            print("Daily Scraper Scheduler: Starting scheduled crawl...")
            subprocess.run([sys.executable, os.path.join(DIRECTORY, "scraper.py")])
            print("Daily Scraper Scheduler: Crawl completed. Reloading Firestore catalog...")
            load_firestore_catalog()
            
        except Exception as e:
            print("Error in daily scraper scheduler:", e)
            time.sleep(60)


class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        pass  # Silence default request logs

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == '/api/search':
            self.handle_api_search(parsed_url.query)
        elif parsed_url.path == '/api/categories':
            self.handle_categories()
        elif parsed_url.path == '/api/scrape-now':
            self.handle_scrape_now()
        else:
            super().do_GET()

    def handle_scrape_now(self):
        def run_async():
            print("Manual scrape triggered...")
            subprocess.run([sys.executable, os.path.join(DIRECTORY, "scraper.py")])
            print("Manual scrape finished. Reloading Firestore catalog...")
            load_firestore_catalog()
            
        threading.Thread(target=run_async, daemon=True).start()
        self.send_json({"status": "Scraper started in the background. Check logs."})

    def send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def handle_categories(self):
        self.send_json(sorted(CATALOG.keys()))

    def handle_api_search(self, query_string):
        try:
            params = urllib.parse.parse_qs(query_string)
            query = params.get('q', [''])[0].strip()

            if not query or len(query) < 2:
                self.send_json({"error": "Query too short"}, 400)
                return

            results = []
            
            # 1. Search in Firestore-loaded catalog
            if FIRESTORE_CATALOG:
                query_lower = query.lower()
                matched_products = []
                # Substring matching on product name or brand
                for cat_key, products in FIRESTORE_CATALOG.items():
                    for product in products:
                        name_lower = product["name"].lower()
                        brand_lower = product["brand"].lower()
                        if query_lower in name_lower or query_lower in brand_lower:
                            matched_products.append((product, cat_key))
                            
                # Format matches
                for idx, (prod, cat_key) in enumerate(matched_products):
                    results.append(make_firestore_result(prod, query, idx, cat_key))
                    
                # If query matches category, load the rest of the products in that category
                cat_key = resolve_catalog_key(query)
                if cat_key and cat_key in FIRESTORE_CATALOG:
                    matched_ids = {r["id"] for r in results}
                    for idx, prod in enumerate(FIRESTORE_CATALOG[cat_key]):
                        if prod["id"] not in matched_ids:
                            results.append(make_firestore_result(prod, query, len(results), cat_key))

            # 2. Fall back to local template CATALOG if no Firestore results found
            if not results:
                cat_key = resolve_catalog_key(query)
                if cat_key and cat_key in CATALOG:
                    templates = CATALOG[cat_key]
                else:
                    # Generative fallback for truly unknown products
                    cap_q = query.capitalize()
                    templates = [
                        {"name": f"{cap_q} Premium Selection 500g",  "brand": "Premium Select",    "size": "500g", "base_price": 15.00},
                        {"name": f"Woolworths {cap_q} Value Pack",   "brand": "Woolworths",        "size": "1kg",  "base_price": 6.50},
                        {"name": f"ALDI {cap_q} House Brand",        "brand": "ALDI",              "size": "500g", "base_price": 4.99},
                        {"name": f"Coles {cap_q} Everyday",          "brand": "Coles",             "size": "500g", "base_price": 5.50},
                    ]
                results = [make_result(t, query, i, cat_key if cat_key else query) for i, t in enumerate(templates)]

            self.send_json(results)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json({"error": str(e)}, 500)


if __name__ == "__main__":
    # Load Firestore catalog (or local scraped fallback)
    load_firestore_catalog()
    
    # Start the 3:00 AM daily scheduler background thread
    threading.Thread(target=run_daily_scheduler, daemon=True).start()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"AussieSaver Backend running --> http://localhost:{PORT}")
        print(f"   Catalog: {len(CATALOG)} categories, {sum(len(v) for v in CATALOG.values())} products")
        print(f"   Aliases: {len(ALIASES)} keyword mappings")
        httpd.serve_forever()
