from collections import OrderedDict


def parse_region_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    # Find the start of Variables and Values sections
    var_start = None
    val_start = None
    for i, line in enumerate(lines):
        if line.strip() == "Variables:":
            var_start = i + 1
        if line.strip() == "Values:":
            val_start = i + 1
            break

    # Parse variables
    variables = []
    i = var_start
    while i < len(lines):
        line = lines[i]
        if line.strip() == "" or line.startswith("Values:"):
            break
        parts = line.strip().split()
        if len(parts) >= 2:
            variables.append(parts[1])
        i += 1

    # Parse values
    values = []
    for line in lines[val_start:]:
        line = line.strip()
        if line == "":
            continue
        # Each value line may have multiple values separated by tabs
        vals = line.split()
        if len(vals) == 2:
            v = vals[-1]
        else:
            v = vals[0]

        try:
            values.append(float(v))
        except ValueError:
            print("error")
            raise ValueError("unknown...")

    # Map variables to values
    region_dict = OrderedDict()
    for var, val in zip(variables, values):
        region_dict[var] = val

    return region_dict


# Example usage:
# region_dict = parse_region_file("Leung_NMCF_region")
# for k, v in region_dict.items():  # print first 10 for demo
#     print(f"{k}: {v}")


# Helper function to determine PMOS region
def get_pmos_region(vgs, vds, vth):
    if abs(vgs) < abs(vth):
        return 0  # cut-off
    else:
        # if abs(vds) < 2 * (abs(vgs) - abs(vth)):
        #     return 3
        if abs(vds) < abs(vgs) - abs(vth):
            return 1  # triode
        else:
            return 2  # saturation


def get_nmos_region(vgs, vds, vth):
    if vgs < vth:
        return 0  # cut-off
    else:
        # if vds < 2 * (vgs - vth):
        #     return 3
        if vds < vgs - vth:
            return 1  # triode
        else:
            return 2  # saturation


region_mapping = {
    0: "cut-off",
    1: "triode",
    2: "saturation",
    3: "deep triode",
    4: "breakdown",
}


def get_device_type(spice_file) -> dict:
    datatype = {}
    with open(spice_file, "r") as f:
        for line in f:
            if "sky130_fd_pr__" not in line or line.startswith("X") == False:
                continue

            data = line.strip().split()
            symbol_name = data[0]
            if symbol_name.startswith("XM"):
                if "pfet" in line:
                    datatype[symbol_name.lower()] = "pfet"
                elif "nfet" in line:
                    datatype[symbol_name.lower()] = "nfet"
    return datatype


def get_working_region_in_text(region_dict: dict, mosfet_type: dict, seperator="\n"):
    devices = region_dict.keys()
    devices = list(set([d.strip().split("_")[-1] for d in devices]))
    devices = [d for d in devices if (d.startswith("xc") != True)]
    devices = [d for d in devices if (d.startswith("v") != True)]
    text_ = ""
    for d in devices:
        vgs = region_dict["vgs_" + d]
        vds = region_dict["vds_" + d]
        vth = region_dict["vth_" + d]
        # print(mosfet_type[d], vgs, vds, vth)
        if mosfet_type[d] == "pfet":
            region = get_pmos_region(vgs, vds, -1.0652)
        if mosfet_type[d] == "nfet":
            region = get_nmos_region(vgs, vds, 0.49439)
        # print(f"{d} is in {region_mapping[region]} region")
        text_ += f"{d} is in {region_mapping[region]}" + seperator
    return text_


def read_region(
    circuit_path="Leung_NMCF.cir", region_file="Leung_NMCF_region", seperator="\n"
):
    region_dict = parse_region_file(region_file)
    # print(region_dict["vgs_xm11"])
    device_type = get_device_type(circuit_path)
    return get_working_region_in_text(region_dict, device_type, seperator)


print(
    read_region(
        circuit_path="Leung_NMCF.cir", region_file="Leung_NMCF_region", seperator=", "
    )
)
