"""C gap 2 producer, explicit Judge FREEZE required before any sealed read."""
from gap1_producer import global_axial_c1b_kernel as kernel
from gap1_producer import global_axial_c1b_gating as gating
from gap2_analysis.endpoint_driver import main

if __name__ == "__main__":
    main("producer", kernel, gating)
