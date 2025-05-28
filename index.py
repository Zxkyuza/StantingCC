import streamlit as st
st.set_page_config(page_title="Aplikasi Perhitungan Status Gizi Anak", layout="centered")
from fpdf import FPDF
import io

st.title("Kalkulator Status Gizi Anak")

# Data standar (hanya sebagian, tambahkan sesuai kebutuhan)
standards = {
    "male": {
        0: {"height": {"median": 48.95, "sd": (51.8 - 46.1) / 3}, "weight": {"median": 3.2, "sd": (3.9 - 2.5) / 3}, "imt": {"median": 12.95, "sd": (14.8 - 11.1) / 3}},
        1: {"height": {"median": 53.75, "sd": (56.7 - 50.8) / 3}, "weight": {"median": 4.25, "sd": (5.1 - 3.4) / 3}, "imt": {"median": 14.35, "sd": (16.3 - 12.4) / 3}},
        2: {"height": {"median": 57.4, "sd": (60.4 - 54.4) / 3}, "weight": {"median": 5.3, "sd": (6.3 - 4.3) / 3}, "imt": {"median": 15.75, "sd": (17.8 - 13.7) / 3}},
        3: {"height": {"median": 60.4, "sd": (63.5 - 57.3) / 3}, "weight": {"median": 6.1, "sd": (7.2 - 5.0) / 3}, "imt": {"median": 16.35, "sd": (18.4 - 14.3) / 3}},
        4: {"height": {"median": 62.85, "sd": (66.0 - 59.7) / 3}, "weight": {"median": 6.7, "sd": (7.8 - 5.6) / 3}, "imt": {"median": 16.6, "sd": (18.7 - 14.5) / 3}},
        5: {"height": {"median": 64.85, "sd": (68.0 - 61.7) / 3}, "weight": {"median": 7.2, "sd": (8.4 - 6.0) / 3}, "imt": {"median": 16.75, "sd": (18.8 - 14.7) / 3}},
        6: {"height": {"median": 66.55, "sd": (69.8 - 63.3) / 3}, "weight": {"median": 7.6, "sd": (8.8 - 6.4) / 3}, "imt": {"median": 16.75, "sd": (18.8 - 14.7) / 3}},
        7: {"height": {"median": 68.05, "sd": (71.3 - 64.8) / 3}, "weight": {"median": 7.95, "sd": (9.2 - 6.7) / 3}, "imt": {"median": 16.8, "sd": (18.8 - 14.8) / 3}},
        8: {"height": {"median": 69.5, "sd": (72.8 - 66.2) / 3}, "weight": {"median": 8.25, "sd": (9.6 - 6.9) / 3}, "imt": {"median": 16.7, "sd": (18.7 - 14.7) / 3}},
        9: {"height": {"median": 70.85, "sd": (74.2 - 67.5) / 3}, "weight": {"median": 8.5, "sd": (9.9 - 7.1) / 3}, "imt": {"median": 16.65, "sd": (18.6 - 14.7) / 3}},
        10: {"height": {"median": 72.15, "sd": (75.6 - 68.7) / 3}, "weight": {"median": 8.8, "sd": (10.2 - 7.4) / 3}, "imt": {"median": 16.55, "sd": (18.5 - 14.6) / 3}},
        11: {"height": {"median": 73.4, "sd": (76.9 - 69.9) / 3}, "weight": {"median": 9.05, "sd": (10.5 - 7.6) / 3}, "imt": {"median": 16.45, "sd": (18.4 - 14.5) / 3}},
        12: {"height": {"median": 74.55, "sd": (78.1 - 71.0) / 3}, "weight": {"median": 9.25, "sd": (10.8 - 7.7) / 3}, "imt": {"median": 16.3, "sd": (18.2 - 14.4) / 3}},
        13: {"height": {"median": 75.7, "sd": (79.3 - 72.1) / 3}, "weight": {"median": 9.45, "sd": (11.0 - 7.9) / 3}, "imt": {"median": 16.2, "sd": (18.1 - 14.3) / 3}},
        14: {"height": {"median": 76.8, "sd": (80.5 - 73.1) / 3}, "weight": {"median": 9.7, "sd": (11.3 - 8.1) / 3}, "imt": {"median": 16.1, "sd": (18.0 - 14.2) / 3}},
        15: {"height": {"median": 77.9, "sd": (81.7 - 74.1) / 3}, "weight": {"median": 9.9, "sd": (11.5 - 8.3) / 3}, "imt": {"median": 15.95, "sd": (17.8 - 14.1) / 3}},
        16: {"height": {"median": 78.9, "sd": (82.8 - 75.0) / 3}, "weight": {"median": 10.05, "sd": (11.7 - 8.4) / 3}, "imt": {"median": 15.85, "sd": (17.7 - 14.0) / 3}},
        17: {"height": {"median": 79.95, "sd": (83.9 - 76.0) / 3}, "weight": {"median": 10.3, "sd": (12.0 - 8.6) / 3}, "imt": {"median": 15.75, "sd": (17.6 - 13.9) / 3}},
        18: {"height": {"median": 80.95, "sd": (85.0 - 76.9) / 3}, "weight": {"median": 10.5, "sd": (12.2 - 8.8) / 3}, "imt": {"median": 15.65, "sd": (17.5 - 13.9) / 3}},
        19: {"height": {"median": 81.85, "sd": (86.0 - 77.7) / 3}, "weight": {"median": 10.7, "sd": (12.5 - 8.9) / 3}, "imt": {"median": 15.6, "sd": (17.4 - 13.8) / 3}},
        20: {"height": {"median": 82.8, "sd": (87.0 - 78.6) / 3}, "weight": {"median": 10.9, "sd": (12.7 - 9.1) / 3}, "imt": {"median": 15.5, "sd": (17.3 - 13.7) / 3}},
        21: {"height": {"median": 83.7, "sd": (88.0 - 79.4) / 3}, "weight": {"median": 11.05, "sd": (12.9 - 9.2) / 3}, "imt": {"median": 15.45, "sd": (17.2 - 13.7) / 3}},
        22: {"height": {"median": 84.6, "sd": (89.0 - 80.2) / 3}, "weight": {"median": 11.3, "sd": (13.2 - 9.4) / 3}, "imt": {"median": 15.4, "sd": (17.2 - 13.6) / 3}},
        23: {"height": {"median": 85.45, "sd": (89.9 - 81.0) / 3}, "weight": {"median": 11.45, "sd": (13.4 - 9.5) / 3}, "imt": {"median": 15.35, "sd": (17.1 - 13.6) / 3}},
        24: {"height": {"median": 86.3, "sd": (90.9 - 81.7) / 3}, "weight": {"median": 11.65, "sd": (13.6 - 9.7) / 3}, "imt": {"median": 15.3, "sd": (17.0 - 13.6) / 3}},
        25: {"height": {"median": 86.4, "sd": (91.1 - 81.7) / 3}, "weight": {"median": 11.85, "sd": (13.9 - 9.8) / 3}, "imt": {"median": 15.55, "sd": (17.3 - 13.8) / 3}},
        26: {"height": {"median": 87.25, "sd": (92.0 - 82.5) / 3}, "weight": {"median": 12.05, "sd": (14.1 - 10.0) / 3}, "imt": {"median": 15.5, "sd": (17.3 - 13.7) / 3}},
        27: {"height": {"median": 88.0, "sd": (92.9 - 83.1) / 3}, "weight": {"median": 12.2, "sd": (14.3 - 10.1) / 3}, "imt": {"median": 15.45, "sd": (17.2 - 13.7) / 3}},
        28: {"height": {"median": 88.75, "sd": (93.7 - 83.8) / 3}, "weight": {"median": 12.35, "sd": (14.5 - 10.2) / 3}, "imt": {"median": 15.4, "sd": (17.2 - 13.6) / 3}},
        29: {"height": {"median": 89.5, "sd": (94.5 - 84.5) / 3}, "weight": {"median": 12.6, "sd": (14.8 - 10.4) / 3}, "imt": {"median": 15.35, "sd": (17.1 - 13.6) / 3}},
        30: {"height": {"median": 90.2, "sd": (95.3 - 85.1) / 3}, "weight": {"median": 12.75, "sd": (15.0 - 10.5) / 3}, "imt": {"median": 15.35, "sd": (17.1 - 13.6) / 3}},
        31: {"height": {"median": 90.9, "sd": (96.1 - 85.7) / 3}, "weight": {"median": 12.95, "sd": (15.2 - 10.7) / 3}, "imt": {"median": 15.3, "sd": (17.1 - 13.5) / 3}},
        32: {"height": {"median": 91.65, "sd": (96.9 - 86.4) / 3}, "weight": {"median": 13.1, "sd": (15.4 - 10.8) / 3}, "imt": {"median": 15.25, "sd": (17.0 - 13.5) / 3}},
        33: {"height": {"median": 92.25, "sd": (97.6 - 86.9) / 3}, "weight": {"median": 13.25, "sd": (15.6 - 10.9) / 3}, "imt": {"median": 15.25, "sd": (17.0 - 13.5) / 3}},
        34: {"height": {"median": 92.95, "sd": (98.4 - 87.5) / 3}, "weight": {"median": 13.4, "sd": (15.8 - 11.0) / 3}, "imt": {"median": 15.2, "sd": (17.0 - 13.4) / 3}},
        35: {"height": {"median": 93.6, "sd": (99.1 - 88.1) / 3}, "weight": {"median": 13.6, "sd": (16.0 - 11.2) / 3}, "imt": {"median": 15.15, "sd": (16.9 - 13.4) / 3}},
        36: {"height": {"median": 94.25, "sd": (99.8 - 88.7) / 3}, "weight": {"median": 13.75, "sd": (16.2 - 11.3) / 3}, "imt": {"median": 15.15, "sd": (16.9 - 13.4) / 3}},
        37: {"height": {"median": 94.85, "sd": (100.5 - 89.2) / 3}, "weight": {"median": 13.9, "sd": (16.4 - 11.4) / 3}, "imt": {"median": 15.1, "sd": (16.9 - 13.3) / 3}},
        38: {"height": {"median": 95.5, "sd": (101.2 - 89.8) / 3}, "weight": {"median": 14.05, "sd": (16.6 - 11.5) / 3}, "imt": {"median": 15.05, "sd": (16.8 - 13.3) / 3}},
        39: {"height": {"median": 96.05, "sd": (101.8 - 90.3) / 3}, "weight": {"median": 14.2, "sd": (16.8 - 11.6) / 3}, "imt": {"median": 15.05, "sd": (16.8 - 13.3) / 3}},
        40: {"height": {"median": 96.7, "sd": (102.5 - 90.9) / 3}, "weight": {"median": 14.4, "sd": (17.0 - 11.8) / 3}, "imt": {"median": 15.0, "sd": (16.8 - 13.2) / 3}},
        41: {"height": {"median": 97.3, "sd": (103.2 - 91.4) / 3}, "weight": {"median": 14.55, "sd": (17.2 - 11.9) / 3}, "imt": {"median": 15.0, "sd": (16.8 - 13.2) / 3}},
        42: {"height": {"median": 97.85, "sd": (103.8 - 91.9) / 3}, "weight": {"median": 14.7, "sd": (17.4 - 12.0) / 3}, "imt": {"median": 15.0, "sd": (16.8 - 13.2) / 3}},
        43: {"height": {"median": 98.45, "sd": (104.5 - 92.4) / 3}, "weight": {"median": 14.85, "sd": (17.6 - 12.1) / 3}, "imt": {"median": 14.95, "sd": (16.7 - 13.2) / 3}},
        44: {"height": {"median": 99.05, "sd": (105.1 - 93.0) / 3}, "weight": {"median": 15.0, "sd": (17.8 - 12.2) / 3}, "imt": {"median": 14.9, "sd": (16.7 - 13.1) / 3}},
        45: {"height": {"median": 99.6, "sd": (105.7 - 93.5) / 3}, "weight": {"median": 15.2, "sd": (18.0 - 12.4) / 3}, "imt": {"median": 14.9, "sd": (16.7 - 13.1) / 3}},
        46: {"height": {"median": 100.15, "sd": (106.3 - 94.0) / 3}, "weight": {"median": 15.35, "sd": (18.2 - 12.5) / 3}, "imt": {"median": 14.9, "sd": (16.7 - 13.1) / 3}},
        47: {"height": {"median": 100.65, "sd": (106.9 - 94.4) / 3}, "weight": {"median": 15.5, "sd": (18.4 - 12.6) / 3}, "imt": {"median": 14.9, "sd": (16.7 - 13.1) / 3}},
        48: {"height": {"median": 101.2, "sd": (107.5 - 94.9) / 3}, "weight": {"median": 15.65, "sd": (18.6 - 12.7) / 3}, "imt": {"median": 14.9, "sd": (16.7 - 13.1) / 3}},
        49: {"height": {"median": 101.75, "sd": (108.1 - 95.4) / 3}, "weight": {"median": 15.8, "sd": (18.8 - 12.8) / 3}, "imt": {"median": 14.85, "sd": (16.7 - 13.0) / 3}},
        50: {"height": {"median": 102.3, "sd": (108.7 - 95.9) / 3}, "weight": {"median": 15.95, "sd": (19.0 - 12.9) / 3}, "imt": {"median": 14.85, "sd": (16.7 - 13.0) / 3}},
        51: {"height": {"median": 102.85, "sd": (109.3 - 96.4) / 3}, "weight": {"median": 16.15, "sd": (19.2 - 13.1) / 3}, "imt": {"median": 14.8, "sd": (16.6 - 13.0) / 3}},
        52: {"height": {"median": 103.4, "sd": (109.9 - 96.9) / 3}, "weight": {"median": 16.3, "sd": (19.4 - 13.2) / 3}, "imt": {"median": 14.8, "sd": (16.6 - 13.0) / 3}},
        53: {"height": {"median": 103.95, "sd": (110.5 - 97.4) / 3}, "weight": {"median": 16.45, "sd": (19.6 - 13.3) / 3}, "imt": {"median": 14.8, "sd": (16.6 - 13.0) / 3}},
        54: {"height": {"median": 104.45, "sd": (111.1 - 97.8) / 3}, "weight": {"median": 16.6, "sd": (19.8 - 13.4) / 3}, "imt": {"median": 14.8, "sd": (16.6 - 13.0) / 3}},
        55: {"height": {"median": 105.0, "sd": (111.7 - 98.3) / 3}, "weight": {"median": 16.75, "sd": (20.0 - 13.5) / 3}, "imt": {"median": 14.8, "sd": (16.6 - 13.0) / 3}},
        56: {"height": {"median": 105.55, "sd": (112.3 - 98.8) / 3}, "weight": {"median": 16.9, "sd": (20.2 - 13.6) / 3}, "imt": {"median": 14.75, "sd": (16.6 - 12.9) / 3}},
        57: {"height": {"median": 106.05, "sd": (112.8 - 99.3) / 3}, "weight": {"median": 17.05, "sd": (20.4 - 13.7) / 3}, "imt": {"median": 14.75, "sd": (16.6 - 12.9) / 3}},
        58: {"height": {"median": 106.55, "sd": (113.4 - 99.7) / 3}, "weight": {"median": 17.2, "sd": (20.6 - 13.8) / 3}, "imt": {"median": 14.75, "sd": (16.6 - 12.9) / 3}},
        59: {"height": {"median": 107.1, "sd": (114.0 - 100.2) / 3}, "weight": {"median": 17.4, "sd": (20.8 - 14.0) / 3}, "imt": {"median": 14.75, "sd": (16.6 - 12.9) / 3}},
        60: {"height": {"median": 107.65, "sd": (114.6 - 100.7) / 3}, "weight": {"median": 17.55, "sd": (21.0 - 14.1) / 3}, "imt": {"median": 14.75, "sd": (16.6 - 12.9) / 3}}
    },
    "female": {
        0: {"height": {"median": 50.05, "sd": (54.7 - 45.4) / 3}, "weight": {"median": 3.05, "sd": (3.7 - 2.4) / 3}, "imt": {"median": 12.85, "sd": (14.6 - 11.1) / 3}},
        1: {"height": {"median": 54.65, "sd": (59.5 - 49.8) / 3}, "weight": {"median": 4.0, "sd": (4.8 - 3.2) / 3}, "imt": {"median": 14.0, "sd": (16.0 - 12.0) / 3}},
        2: {"height": {"median": 58.1, "sd": (63.2 - 53.0) / 3}, "weight": {"median": 4.85, "sd": (5.8 - 3.9) / 3}, "imt": {"median": 15.15, "sd": (17.3 - 13.0) / 3}},
        3: {"height": {"median": 60.85, "sd": (66.1 - 55.6) / 3}, "weight": {"median": 5.55, "sd": (6.6 - 4.5) / 3}, "imt": {"median": 15.75, "sd": (17.9 - 13.6) / 3}},
        4: {"height": {"median": 63.2, "sd": (68.6 - 57.8) / 3}, "weight": {"median": 6.15, "sd": (7.3 - 5.0) / 3}, "imt": {"median": 16.1, "sd": (18.3 - 13.9) / 3}},
        5: {"height": {"median": 65.15, "sd": (70.7 - 59.6) / 3}, "weight": {"median": 6.6, "sd": (7.8 - 5.4) / 3}, "imt": {"median": 16.25, "sd": (18.4 - 14.1) / 3}},
        6: {"height": {"median": 66.85, "sd": (72.5 - 61.2) / 3}, "weight": {"median": 7.0, "sd": (8.2 - 5.7) / 3}, "imt": {"median": 16.3, "sd": (18.5 - 14.1) / 3}},
        7: {"height": {"median": 68.45, "sd": (74.2 - 62.7) / 3}, "weight": {"median": 7.3, "sd": (8.6 - 6.0) / 3}, "imt": {"median": 16.35, "sd": (18.5 - 14.2) / 3}},
        8: {"height": {"median": 69.9, "sd": (75.8 - 64.0) / 3}, "weight": {"median": 7.65, "sd": (9.0 - 6.3) / 3}, "imt": {"median": 16.25, "sd": (18.4 - 14.1) / 3}},
        9: {"height": {"median": 71.35, "sd": (77.4 - 65.3) / 3}, "weight": {"median": 7.9, "sd": (9.3 - 6.5) / 3}, "imt": {"median": 16.2, "sd": (18.3 - 14.1) / 3}},
        10: {"height": {"median": 72.7, "sd": (78.9 - 66.5) / 3}, "weight": {"median": 8.15, "sd": (9.6 - 6.7) / 3}, "imt": {"median": 16.1, "sd": (18.2 - 14.0) / 3}},
        11: {"height": {"median": 74.0, "sd": (80.3 - 67.7) / 3}, "weight": {"median": 8.4, "sd": (9.9 - 6.9) / 3}, "imt": {"median": 15.95, "sd": (18.0 - 13.9) / 3}},
        12: {"height": {"median": 75.3, "sd": (81.7 - 68.9) / 3}, "weight": {"median": 8.55, "sd": (10.1 - 7.0) / 3}, "imt": {"median": 15.85, "sd": (17.9 - 13.8) / 3}},
        13: {"height": {"median": 76.55, "sd": (83.1 - 70.0) / 3}, "weight": {"median": 8.8, "sd": (10.4 - 7.2) / 3}, "imt": {"median": 15.7, "sd": (17.7 - 13.7) / 3}},
        14: {"height": {"median": 77.7, "sd": (84.4 - 71.0) / 3}, "weight": {"median": 9.0, "sd": (10.6 - 7.4) / 3}, "imt": {"median": 15.6, "sd": (17.6 - 13.6) / 3}},
        15: {"height": {"median": 78.85, "sd": (85.7 - 72.0) / 3}, "weight": {"median": 9.25, "sd": (10.9 - 7.6) / 3}, "imt": {"median": 15.5, "sd": (17.5 - 13.5) / 3}},
        16: {"height": {"median": 80.0, "sd": (87.0 - 73.0) / 3}, "weight": {"median": 9.4, "sd": (11.1 - 7.7) / 3}, "imt": {"median": 15.45, "sd": (17.4 - 13.5) / 3}},
        17: {"height": {"median": 81.1, "sd": (88.2 - 74.0) / 3}, "weight": {"median": 9.65, "sd": (11.4 - 7.9) / 3}, "imt": {"median": 15.35, "sd": (17.3 - 13.4) / 3}},
        18: {"height": {"median": 82.15, "sd": (89.4 - 74.9) / 3}, "weight": {"median": 9.85, "sd": (11.6 - 8.1) / 3}, "imt": {"median": 15.25, "sd": (17.2 - 13.3) / 3}},
        19: {"height": {"median": 83.2, "sd": (90.6 - 75.8) / 3}, "weight": {"median": 10.0, "sd": (11.8 - 8.2) / 3}, "imt": {"median": 15.2, "sd": (17.1 - 13.3) / 3}},
        20: {"height": {"median": 84.2, "sd": (91.7 - 76.7) / 3}, "weight": {"median": 10.25, "sd": (12.1 - 8.4) / 3}, "imt": {"median": 15.1, "sd": (17.0 - 13.2) / 3}},
        21: {"height": {"median": 85.2, "sd": (92.9 - 77.5) / 3}, "weight": {"median": 10.45, "sd": (12.3 - 8.6) / 3}, "imt": {"median": 15.1, "sd": (17.0 - 13.2) / 3}},
        22: {"height": {"median": 86.2, "sd": (94.0 - 78.4) / 3}, "weight": {"median": 10.6, "sd": (12.5 - 8.7) / 3}, "imt": {"median": 15.0, "sd": (16.9 - 13.1) / 3}},
        23: {"height": {"median": 87.1, "sd": (95.0 - 79.2) / 3}, "weight": {"median": 10.85, "sd": (12.8 - 8.9) / 3}, "imt": {"median": 15.0, "sd": (16.9 - 13.1) / 3}},
        24: {"height": {"median": 88.05, "sd": (96.1 - 80.0) / 3}, "weight": {"median": 11.0, "sd": (13.0 - 9.0) / 3}, "imt": {"median": 14.95, "sd": (16.8 - 13.1) / 3}},
        25: {"height": {"median": 88.2, "sd": (96.4 - 80.0) / 3}, "weight": {"median": 11.25, "sd": (13.3 - 9.2) / 3}, "imt": {"median": 15.2, "sd": (17.1 - 13.3) / 3}},
        26: {"height": {"median": 89.1, "sd": (97.4 - 80.8) / 3}, "weight": {"median": 11.45, "sd": (13.5 - 9.4) / 3}, "imt": {"median": 15.15, "sd": (17.0 - 13.3) / 3}},
        27: {"height": {"median": 89.95, "sd": (98.4 - 81.5) / 3}, "weight": {"median": 11.6, "sd": (13.7 - 9.5) / 3}, "imt": {"median": 15.15, "sd": (17.0 - 13.3) / 3}},
        28: {"height": {"median": 90.8, "sd": (99.4 - 82.2) / 3}, "weight": {"median": 11.85, "sd": (14.0 - 9.7) / 3}, "imt": {"median": 15.15, "sd": (17.0 - 13.3) / 3}},
        29: {"height": {"median": 91.6, "sd": (100.3 - 82.9) / 3}, "weight": {"median": 12.0, "sd": (14.2 - 9.8) / 3}, "imt": {"median": 15.1, "sd": (17.0 - 13.2) / 3}},
        30: {"height": {"median": 92.45, "sd": (101.3 - 83.6) / 3}, "weight": {"median": 12.2, "sd": (14.4 - 10.0) / 3}, "imt": {"median": 15.05, "sd": (16.9 - 13.2) / 3}},
        31: {"height": {"median": 93.25, "sd": (102.2 - 84.3) / 3}, "weight": {"median": 12.4, "sd": (14.7 - 10.1) / 3}, "imt": {"median": 15.05, "sd": (16.9 - 13.2) / 3}},
        32: {"height": {"median": 94.0, "sd": (103.1 - 84.9) / 3}, "weight": {"median": 12.6, "sd": (14.9 - 10.3) / 3}, "imt": {"median": 15.05, "sd": (16.9 - 13.2) / 3}},
        33: {"height": {"median": 94.75, "sd": (103.9 - 85.6) / 3}, "weight": {"median": 12.75, "sd": (15.1 - 10.4) / 3}, "imt": {"median": 15.0, "sd": (16.9 - 13.1) / 3}},
        34: {"height": {"median": 95.5, "sd": (104.8 - 86.2) / 3}, "weight": {"median": 12.95, "sd": (15.4 - 10.5) / 3}, "imt": {"median": 14.95, "sd": (16.8 - 13.1) / 3}},
        35: {"height": {"median": 96.2, "sd": (105.6 - 86.8) / 3}, "weight": {"median": 13.15, "sd": (15.6 - 10.7) / 3}, "imt": {"median": 14.95, "sd": (16.8 - 13.1) / 3}},
        36: {"height": {"median": 96.95, "sd": (106.5 - 87.4) / 3}, "weight": {"median": 13.3, "sd": (15.8 - 10.8) / 3}, "imt": {"median": 14.95, "sd": (16.8 - 13.1) / 3}},
        37: {"height": {"median": 97.65, "sd": (107.3 - 88.0) / 3}, "weight": {"median": 13.45, "sd": (16.0 - 10.9) / 3}, "imt": {"median": 14.95, "sd": (16.8 - 13.1) / 3}},
        38: {"height": {"median": 98.35, "sd": (108.1 - 88.6) / 3}, "weight": {"median": 13.7, "sd": (16.3 - 11.1) / 3}, "imt": {"median": 14.9, "sd": (16.8 - 13.0) / 3}},
        39: {"height": {"median": 99.05, "sd": (108.9 - 89.2) / 3}, "weight": {"median": 13.85, "sd": (16.5 - 11.2) / 3}, "imt": {"median": 14.9, "sd": (16.8 - 13.0) / 3}},
        40: {"height": {"median": 99.75, "sd": (109.7 - 89.8) / 3}, "weight": {"median": 14.0, "sd": (16.7 - 11.3) / 3}, "imt": {"median": 14.9, "sd": (16.8 - 13.0) / 3}},
        41: {"height": {"median": 100.45, "sd": (110.5 - 90.4) / 3}, "weight": {"median": 14.2, "sd": (16.9 - 11.5) / 3}, "imt": {"median": 14.9, "sd": (16.8 - 13.0) / 3}},
        42: {"height": {"median": 101.05, "sd": (111.2 - 90.9) / 3}, "weight": {"median": 14.4, "sd": (17.2 - 11.6) / 3}, "imt": {"median": 14.85, "sd": (16.8 - 12.9) / 3}},
        43: {"height": {"median": 101.75, "sd": (112.0 - 91.5) / 3}, "weight": {"median": 14.55, "sd": (17.4 - 11.7) / 3}, "imt": {"median": 14.85, "sd": (16.8 - 12.9) / 3}},
        44: {"height": {"median": 102.35, "sd": (112.7 - 92.0) / 3}, "weight": {"median": 14.7, "sd": (17.6 - 11.8) / 3}, "imt": {"median": 14.85, "sd": (16.8 - 12.9) / 3}},
        45: {"height": {"median": 103.0, "sd": (113.5 - 92.5) / 3}, "weight": {"median": 14.9, "sd": (17.8 - 12.0) / 3}, "imt": {"median": 14.85, "sd": (16.8 - 12.9) / 3}},
        46: {"height": {"median": 103.65, "sd": (114.2 - 93.1) / 3}, "weight": {"median": 15.1, "sd": (18.1 - 12.1) / 3}, "imt": {"median": 14.85, "sd": (16.8 - 12.9) / 3}},
        47: {"height": {"median": 104.25, "sd": (114.9 - 93.6) / 3}, "weight": {"median": 15.25, "sd": (18.3 - 12.2) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        48: {"height": {"median": 104.9, "sd": (115.7 - 94.1) / 3}, "weight": {"median": 15.4, "sd": (18.5 - 12.3) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        49: {"height": {"median": 105.5, "sd": (116.4 - 94.6) / 3}, "weight": {"median": 15.6, "sd": (18.8 - 12.4) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        50: {"height": {"median": 106.1, "sd": (117.1 - 95.1) / 3}, "weight": {"median": 15.8, "sd": (19.0 - 12.6) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        51: {"height": {"median": 106.65, "sd": (117.7 - 95.6) / 3}, "weight": {"median": 15.95, "sd": (19.2 - 12.7) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        52: {"height": {"median": 107.25, "sd": (118.4 - 96.1) / 3}, "weight": {"median": 16.1, "sd": (19.4 - 12.8) / 3}, "imt": {"median": 14.8, "sd": (16.8 - 12.8) / 3}},
        53: {"height": {"median": 107.85, "sd": (119.1 - 96.6) / 3}, "weight": {"median": 16.3, "sd": (19.7 - 12.9) / 3}, "imt": {"median": 14.75, "sd": (16.8 - 12.7) / 3}},
        54: {"height": {"median": 108.45, "sd": (119.8 - 97.1) / 3}, "weight": {"median": 16.45, "sd": (19.9 - 13.0) / 3}, "imt": {"median": 14.75, "sd": (16.8 - 12.7) / 3}},
        55: {"height": {"median": 109.0, "sd": (120.4 - 97.6) / 3}, "weight": {"median": 16.65, "sd": (20.1 - 13.2) / 3}, "imt": {"median": 14.75, "sd": (16.8 - 12.7) / 3}},
        56: {"height": {"median": 109.6, "sd": (121.1 - 98.1) / 3}, "weight": {"median": 16.8, "sd": (20.3 - 13.3) / 3}, "imt": {"median": 14.75, "sd": (16.8 - 12.7) / 3}},
        57: {"height": {"median": 110.15, "sd": (121.8 - 98.5) / 3}, "weight": {"median": 17.0, "sd": (20.6 - 13.4) / 3}, "imt": {"median": 14.8, "sd": (16.9 - 12.7) / 3}},
        58: {"height": {"median": 110.7, "sd": (122.4 - 99.0) / 3}, "weight": {"median": 17.15, "sd": (20.8 - 13.5) / 3}, "imt": {"median": 14.8, "sd": (16.9 - 12.7) / 3}},
        59: {"height": {"median": 111.3, "sd": (123.1 - 99.5) / 3}, "weight": {"median": 17.3, "sd": (21.0 - 13.6) / 3}, "imt": {"median": 14.8, "sd": (16.9 - 12.7) / 3}},
        60: {"height": {"median": 111.8, "sd": (123.7 - 99.9) / 3}, "weight": {"median": 17.45, "sd": (21.2 - 13.7) / 3}, "imt": {"median": 14.8, "sd": (16.9 - 12.7) / 3}}
    }
}

gender = st.selectbox("Jenis Kelamin", options=["Laki-laki", "Perempuan"])
gender_key = "male" if gender == "Laki-laki" else "female"
age = st.number_input("Usia (bulan)", min_value=0, max_value=60, step=1)
height = st.number_input("Tinggi Badan (cm)", min_value=0.0, step=0.1, format="%.1f")
weight = st.number_input("Berat Badan (kg)", min_value=0.0, step=0.1, format="%.1f")

result = ""
imt = 0.0

if st.button("Hitung"):
    with st.spinner("Menghitung..."):
        if age not in standards[gender_key]:
            st.error("Data standar untuk usia ini belum tersedia. Silakan masukkan usia antara 0-60 bulan.")
        elif height <= 0 or weight <= 0:
            st.error("Tinggi badan dan berat badan harus lebih dari 0.")
        elif height > 150 or weight > 50:
            st.error("Tinggi badan atau berat badan tidak realistis untuk anak usia 0-60 bulan.")
        else:
            data = standards[gender_key][age]
            zHeight = (height - data["height"]["median"]) / data["height"]["sd"]
            zWeight = (weight - data["weight"]["median"]) / data["weight"]["sd"]
            imt = weight / ((height / 100) ** 2)
            zImt = (imt - data["imt"]["median"]) / data["imt"]["sd"]

            # Status BB/U
            if zWeight < -3:
                statusWeight = 'Sangat Kurang'
            elif -3 <= zWeight < -2:
                statusWeight = 'Kurang'
            elif -2 <= zWeight <= 1:
                statusWeight = 'Normal'
            else:
                statusWeight = 'Risiko Berlebih'

            # Status TB/U
            if zHeight < -3:
                statusHeight = 'Sangat Pendek (Stunting Berat)'
            elif -3 <= zHeight < -2:
                statusHeight = 'Pendek (Stunting)'
            elif -2 <= zHeight <= 3:
                statusHeight = 'Normal'
            else:
                statusHeight = 'Tinggi (Risiko Berlebih)'

            # Status IMT/U
            if zImt < -3:
                statusImt = 'Gizi Buruk'
            elif -3 <= zImt < -2:
                statusImt = 'Gizi Kurang'
            elif -2 <= zImt <= 1:
                statusImt = 'Gizi Baik'
            elif 1 < zImt <= 2:
                statusImt = 'Berisiko Gizi Lebih'
            elif 2 < zImt <= 3:
                statusImt = 'Gizi Lebih'
            else:
                statusImt = 'Obesitas'

            result = (
                f"**Status BB/U:** {statusWeight}\n"
                f"**Status TB/U:** {statusHeight}\n"
                f"**IMT/U:** {imt:.2f}\n"
                f"**Status IMT/U:** {statusImt}"
            )
            st.markdown(result)

            # PDF generation
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, "Hasil Status Gizi Anak", ln=True)
            pdf.cell(0, 10, f"Jenis Kelamin: {gender}", ln=True)
            pdf.cell(0, 10, f"Usia (bulan): {age}", ln=True)
            pdf.cell(0, 10, f"Tinggi Badan (cm): {height}", ln=True)
            pdf.cell(0, 10, f"Berat Badan (kg): {weight}", ln=True)
            pdf.cell(0, 10, f"Status BB/U: {statusWeight}", ln=True)
            pdf.cell(0, 10, f"Status TB/U: {statusHeight}", ln=True)
            pdf.cell(0, 10, f"IMT/U: {imt:.2f}", ln=True)
            pdf.cell(0, 10, f"Status IMT/U: {statusImt}", ln=True)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            st.download_button(
                label="Download PDF",
                data=pdf_output,
                file_name="status-gizi-anak.pdf",
                mime="application/pdf"
            )
