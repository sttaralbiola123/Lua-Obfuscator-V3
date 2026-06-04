import random

def random_string(length=12):
    """Generates a confusing sequence of i, l, I, 1 to throw off readers"""
    chars = ['i', 'l', 'I', '1']
    # Ensure it starts with a letter so it remains a valid variable name
    start_char = random.choice(['i', 'l', 'I'])
    return start_char + "".join(random.choice(chars) for _ in range(length - 1))

def hex_encode_string(source_str: str) -> str:
    """Converts a standard text string into raw Lua byte escape codes (\\xXX)"""
    return "".join(f"\\x{ord(c):02x}" for c in source_str)

def process_code(source_code: str, intensity: str = "extreme") -> str:
    """
    Transforms standard Lua/Luau script into a layered configuration 
    using hex representation, string mangling, and optional variable obfuscation.
    """
    if not source_code.strip():
        raise ValueError("Walang laman ang code na iyong ipinasok!")

    if len(source_code) > 150000:
        raise ValueError("Masyadong malaki ang source code. Limitado ito sa 150,000 characters.")

    # 1. Obfuscate the primary content string into HEX
    hex_bytecode = hex_encode_string(source_code)

    # 2. Build obfuscated runtime variables
    vm_table_name = random_string(10)
    bytecode_var = random_string(12)
    loader_func = random_string(11)
    arg_name = random_string(6)

    # 3. Handle layered structural configurations based on intensity chosen
    junk_layers = ""
    if intensity in ["medium", "extreme"]:
        # Insert randomized dynamic lookups that evaluate but perform no destructive acts
        j_var1 = random_string(14)
        junk_layers += f"local {j_var1} = {{ {random.randint(10,99)}, {random.randint(100,999)}, ['{random_string(4)}'] = true }};
"
        junk_layers += f"for _ = 1, 3 do table.insert({j_var1}, string.byte('S')) end
"
        
    if intensity == "extreme":
        # Multi-layer layout generation
        j_var2 = random_string(15)
        junk_layers += f"local {j_var2} = function()
"
        junk_layers += f"    local temp = string.reverse('{random_string(5)}')
"
        junk_layers += f"    return #temp > 0
"
        junk_layers += f"end;
"
        junk_layers += f"if not {j_var2}() then return nil end
"

    # 4. Generate the fully operational runtime execution payload block
    custom_obfuscated_template = f"""--[[ 
    STTAR OBFUSCATOR PREMIUM v2
    [PROTECTION LEVEL: {intensity.upper()}]
    Fully Optimized for Top Tier Lua 5.1/Luau Execution Environments.
--]]

{junk_layers}
local {vm_table_name} = {{}}
local {bytecode_var} = "{hex_bytecode}"

local function {loader_func}({arg_name})
    local runtime_env = setmetatable({{}}, {{__index = getfenv()}})
    local compile_success, executable_block = pcall(function()
        return loadstring({bytecode_var})
    end)
    
    if compile_success and executable_block then
        setfenv(executable_block, runtime_env)
        return executable_block
    else
        error("Decryption pipeline failed or payload corrupted.")
    end
end

local core_execution_gate = {loader_func}()
if core_execution_gate then
    core_execution_gate()
else
    print("Execution halt under Sttar isolation container.")
end
"""
    return custom_obfuscated_template
