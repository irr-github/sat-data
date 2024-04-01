TRUECOLOR = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

TRUECOLOR_CLM = """
    //VERSION=3
    function setup() {
    return {
        input: ["B02", "B03", "B04", "CLM"],
        output: { bands: 3 }
    }
    }

    function evaluatePixel(sample) {
    if (sample.CLM == 1) {
        return [4* + sample.B04, sample.B03, sample.B02]
    }
    return [sample.B04, sample.B03, sample.B02];
    } 
"""

SWIR16 = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B11"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B11];
    }
"""


def gen_eval_script(bands_list=["B02"]):
    """experimental script maker"""

    bands_list = ["B02", "B03", "B04"]
    bands_list_str = str(bands_list)
    n_bands = len(bands_list)
    eval_ = str(["sample." + band for band in bands_list])
    eval_ = eval_.replace("'", "")  # remove the quote marks
    script = f"""
        //VERSION=3
    
        function setup() {{
            return {{
                input: [{{
                    bands: {bands_list_str}
                }}],
                output: {{
                    bands: {n_bands}
                }}
            }};
        }}

        function evaluatePixel(sample) {{
            return {eval_};
        }}
    """
    return script
