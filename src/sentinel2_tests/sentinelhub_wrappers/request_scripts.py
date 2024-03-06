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


def gen_L1c_eval_script(bands_list = ['B02'], CLM = False):
    
    n_bands = len(bands_list)
    if CLM:
        bands_list += [CLM]
        
    script = """
    //VERSION=3
    function setup() {
    return {
    """
    script+= f"    input: {bands_list}"
    script += f"    output: {{bands: {n_bands} }}"
    script += """
        }
        }

        function evaluatePixel(sample) {
        if (sample.CLM == 1) {
            return [4* + sample.B04, sample.B03, sample.B02]
        }
        return [sample.B04, sample.B03, sample.B02];
        } 
    """
    
    return script