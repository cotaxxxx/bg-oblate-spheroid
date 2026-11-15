"""C gap 2 independent checker, not a consumer of producer sign decisions."""
from gap1_checker import global_axial_c1b_kernel as kernel
from gap1_checker import global_axial_c1b_gating as gating
from gap2_analysis.endpoint_driver import main

if __name__ == "__main__":
    main("checker", kernel, gating)
