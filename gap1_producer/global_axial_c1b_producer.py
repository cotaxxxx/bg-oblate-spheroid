#!/usr/bin/env python3
from gap1_producer import global_axial_c1b_kernel as kernel
from gap1_producer import global_axial_c1b_gating as gating
from gap1_analysis import c1b_resumable_driver as persistence
if __name__ == "__main__":
    gating.main(kernel, "producer")
