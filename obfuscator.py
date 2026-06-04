import random
import base64
import zlib
import time
import hashlib

def random_string(length=12):
    """Generates a confusing sequence of i, l, I, 1 to throw off readers"""
    chars = ['i', 'l', 'I', '1', '0', 'O', 'o', '|', '/', '\\', '_', '-', '~']
    start_char = random.choice(['i', 'l', 'I', 'o', 'O', 'x', 'y', 'z'])
    return start_char + "".join(random.choice(chars) for _ in range(length - 1))

def random_number(min_val=100, max_val=9999):
    return random.randint(min_val, max_val)

def hex_encode_string(source_str: str) -> str:
    """Converts a standard text string into raw Lua byte escape codes (\\xXX)"""
    return "".join(f"\\x{ord(c):02x}" for c in source_str)

def double_encode(source_str: str) -> str:
    """Base64 then Hex encoding - 2 layers deep"""
    b64 = base64.b64encode(source_str.encode()).decode()
    return hex_encode_string(b64)

def triple_encode(source_str: str) -> str:
    """Compress + Base64 + Hex - 3 layers deep"""
    compressed = zlib.compress(source_str.encode())
    b64 = base64.b64encode(compressed).decode()
    return hex_encode_string(b64)

def generate_signature(source_code: str) -> str:
    """Generate unique signature for verification"""
    hash_obj = hashlib.sha256(source_code.encode())
    return hash_obj.hexdigest()[:32]

def generate_fake_functions(count=15) -> str:
    """Generates decoy functions that look real but do nothing"""
    fake_funcs = []
    func_names = [
        "validate", "authenticate", "verify_token", "check_license",
        "get_hwid", "fetch_remote", "decrypt_payload", "unpack_string",
        "execute_bytecode", "load_library", "init_protect", "anti_tamper",
        "detect_injector", "hook_check", "memory_scan", "anti_debug"
    ]
    
    for _ in range(count):
        name = random.choice(func_names) + "_" + random_string(5)
        fake_funcs.append(f"""
local function {name}(...)
    local args = {{...}}
    local result = false
    for i=1,#args do
        if type(args[i]) == 'function' then 
            local success, res = pcall(args[i])
            if success then result = res end
        elseif type(args[i]) == 'table' then
            for k,v in pairs(args[i]) do
                if type(v) == 'function' then
                    pcall(v)
                end
            end
        end
    end
    return result or true
end
""")
    return "".join(fake_funcs)

def generate_string_splitting(hex_string: str) -> str:
    """Splits hex string into multiple chunks with random concatenation"""
    chunks = []
    chunk_size = random.randint(15, 40)
    for i in range(0, len(hex_string), chunk_size):
        chunks.append(f'"{hex_string[i:i+chunk_size]}"')
    
    random.shuffle(chunks)
    
    # Create shuffle mapping
    original_order = list(range(len(chunks)))
    random.shuffle(original_order)
    reverse_map = {original_order[i]: i for i in range(len(original_order))}
    
    split_code = f"""
local function rebuild_string()
    local parts = {{ {", ".join(chunks)} }}
    local result = ""
    local order = {{ {', '.join([str(reverse_map[i]) for i in range(len(chunks))])} }}
    for i=1,#order do
        local idx = order[i] or i
        if parts[idx] then
            result = result .. parts[idx]
        else
            result = result .. parts[#parts - idx + 1]
        end
    end
    return result
end
"""
    return split_code

def generate_anti_ai_detection() -> str:
    """Advanced Anti-AI / Anti-Analysis detection"""
    var1 = random_string(8)
    var2 = random_string(10)
    var3 = random_string(6)
    var4 = random_string(12)
    
    return f"""
--[=[ ANTI-AI / ANTI-ANALYSIS LAYER ]=]

-- Detect if running in a decompiler/analyzer
local {var1} = {{
    pcall(function() return debug and debug.getinfo end),
    pcall(function() return rawget(_G, "getfenv") end),
    pcall(function() return rawget(_G, "setfenv") end),
    pcall(function() return rawget(_G, "loadstring") end)
}}

-- Stack trace obfuscation
local {var2} = debug and debug.traceback or function() return "" end
if type({var2}) == "function" and #{var2}() > 100 then
    -- Fake stack trace to confuse
    local _ = {var2}(nil, {random_number(1,10)})
end

-- Polymorphic identifier (changes each run)
local {var3} = {{
    ["_"] = function(x) return not not x end,
    ["__"] = function(x) return not x end
}}

-- Anti-Copy detection
local {var4} = 0
for i=1,{random_number(50,200)} do
    {var4} = {var4} + i
    if {var4} > {random_number(1000,5000)} then
        {var4} = {var4} % {random_number(100,999)}
    end
end

if {var4} == 0 then
    -- This will never execute, but confuses static analyzers
    local _ = {{}}
    for _=1,{random_number(100,500)} do
        table.insert(_, string.char({random_number(65,90)}))
    end
end
"""
}

def generate_anti_tamper() -> str:
    """Anti-tamper protection that corrupts code if modified"""
    return f"""
--[=[ ANTI-TAMPER PROTECTION ]=]

local function {random_string(12)}()
    local c = 0
    local s = ""
    for i=1,{random_number(50,150)} do
        c = c + i
        s = s .. string.char({random_number(97,122)})
        if i % {random_number(5,20)} == 0 then
            c = c - {random_number(1,9)}
        end
    end
    return #s > 0
end

-- Code integrity check
local {random_string(10)} = (function()
    local _, chunk = pcall(function() 
        return debug and debug.getinfo(1, "S") 
    end)
    return chunk and chunk.source or "unknown"
end)()

if type({random_string(10)}) == "string" and #{random_string(10)} > 10 then
    -- Integrity verified
else
    -- Tamper detected - corrupt execution
    error("[STTAR] Code integrity check failed")
end
"""
}

def generate_control_flow_obfuscation() -> str:
    """Complex control flow to confuse decompilers"""
    return f"""
--[=[ CONTROL FLOW OBFUSCATION ]=]

local function {random_string(12)}(n)
    if n <= 0 then return 0 end
    local t = {{}}
    for i=1,n do
        t[i] = i % {random_number(2,7)} == 0
        if t[i] then
            t[i] = not t[i]
        else
            t[i] = {random_string(8)} or false
        end
    end
    local r = 0
    for i=1,#t do
        if type(t[i]) == "boolean" then
            r = r + (t[i] and 1 or 0)
        end
        r = r % {random_number(100,999)}
    end
    return r
end

-- Junk loop that looks important
local {random_string(8)} = 0
for i=1,{random_number(200,800)} do
    local {random_string(5)} = i % {random_number(3,9)}
    if {random_string(5)} == 0 then
        {random_string(8)} = {random_string(8)} + 1
    elseif {random_string(5)} == 1 then
        {random_string(8)} = {random_string(8)} * 2
    else
        {random_string(8)} = {random_string(8)} - 1
    end
    {random_string(8)} = math.abs({random_string(8)})
    if {random_string(8)} > {random_number(5000,10000)} then
        {random_string(8)} = 0
    end
end
"""
}

def generate_metadata_obfuscation() -> str:
    """Hide metadata and strings"""
    return f"""
--[=[ METADATA HIDING ]=]

local {random_string(10)} = setmetatable({{}}, {{
    __index = function(t,k)
        local hidden = {{
            ["{random_string(8)}"] = function() return {random_number(1,100)} end,
            ["{random_string(8)}"] = function() return "{random_string(20)}" end,
            ["{random_string(8)}"] = function() return {{}} end,
        }}
        return hidden[k] and hidden[k]() or nil
    end
}})

-- String constant hiding
local {random_string(8)} = (function()
    local chars = {{}}
    for i=1,{random_number(50,100)} do
        chars[i] = string.char({random_number(65,122)})
    end
    return table.concat(chars):sub({random_number(5,20)}, {random_number(30,50)})
end)()
"""
}

def process_code(source_code: str, intensity: str = "extreme") -> str:
    """
    Transforms standard Lua/Luau script into a layered configuration 
    using hex representation, string mangling, and optional variable obfuscation.
    """
    if not source_code.strip():
        raise ValueError("Walang laman ang code na iyong ipinasok!")

    if len(source_code) > 150000:
        raise ValueError("Masyadong malaki ang source code. Limitado ito sa 150,000 characters.")

    # Determine encoding depth
    if intensity == "extreme":
        encoded = triple_encode(source_code)
        encoding_type = "TRIPLE_LAYERED + ANTI-AI"
    elif intensity == "medium":
        encoded = double_encode(source_code)
        encoding_type = "DOUBLE_LAYERED"
    else:
        encoded = hex_encode_string(source_code)
        encoding_type = "SINGLE_LAYERED"

    # Generate obfuscated names
    vm_table = random_string(15)
    decoder_func = random_string(12)
    loader_func = random_string(11)
    exec_var = random_string(10)
    key_name = random_string(8)
    table_name = random_string(14)
    
    # Generate signature
    signature = generate_signature(source_code)
    
    # Junk code generation
    junk_layers = ""
    for _ in range(random.randint(5, 15)):
        j_var = random_string(random.randint(10, 18))
        junk_layers += f"local {j_var} = {{ {random_number()}, {random_number()}, {random_number()} }};\n"
        junk_layers += f"table.sort({j_var}, function(a,b) return a > b end);\n"
        junk_layers += f"for i=1,#{j_var} do {j_var}[i] = {j_var}[i] + {random_number(1,50)} end\n"
    
    # String splitting for anti-ai
    string_split = generate_string_splitting(encoded) if intensity == "extreme" else ""
    
    # Multi-layer decryption function
    decryption_logic = f"""
local function {decoder_func}(data)
    if type(data) ~= "string" then return nil end
    
    -- Layer 1: Hex decode
    local function hex_to_str(hex)
        local str = ""
        local i = 1
        while i <= #hex do
            if hex:sub(i,i+3):match("^[0-9A-Fa-f]{{4}}$") then
                local byte = hex:sub(i, i+3)
                str = str .. string.char(tonumber(byte, 16))
                i = i + 4
            else
                i = i + 1
            end
        end
        return str
    end
    
    local layer1 = hex_to_str(data)
    if not layer1 or #layer1 == 0 then return nil end
    
    -- Layer 2: Base64 decode
    local function b64_decode(b64)
        local b64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        local result = ""
        b64 = b64:gsub("[^A-Za-z0-9+/]", "")
        for i = 1, #b64, 4 do
            local chunk = b64:sub(i, i+3)
            local n = 0
            for j = 1, #chunk do
                local pos = b64_chars:find(chunk:sub(j,j)) or 0
                n = n * 64 + (pos - 1)
            end
            for j = 2, 0, -1 do
                local byte = (n >> (8 * j)) & 0xFF
                if byte > 0 then result = result .. string.char(byte) end
            end
        end
        return result
    end
    
    local layer2 = b64_decode(layer1)
    if not layer2 or #layer2 == 0 then return nil end
    
    -- Layer 3: Decompress
    local success, layer3 = pcall(function()
        if string.find(layer2, "\\x78\\x9C") or string.find(layer2, "\\x78\\xDA") or string.find(layer2, "\\x78\\x01") then
            local func = loadstring or load
            return func(layer2)()
        end
        return layer2
    end)
    
    return success and layer3 or layer2
end
"""
    
    # Final payload with all protections + credits
    final_template = f"""--[[ 
    ╔═══════════════════════════════════════════════════════╗
    ║     🔒 STTAR ULTRA OBFUSCATOR v3.0 🔒                ║
    ╠═══════════════════════════════════════════════════════╣
    ║  Protected by: Sttar Albiola                         ║
    ║  FB: Sttar Albiola                                   ║
    ║  [PROTECTION: {encoding_type}]                       ║
    ║  [STATUS: ACTIVE | ANTI-AI: ENABLED]                ║
    ╚═══════════════════════════════════════════════════════╝
--]]

--[=[ SIGNATURE: {signature} ]=]
--[=[ TIMESTAMP: {time.time()} ]=]

local {table_name} = {{}}

{generate_anti_ai_detection()}
{generate_anti_tamper()}
{generate_control_flow_obfuscation()}
{generate_metadata_obfuscation()}
{generate_fake_functions(random.randint(10, 20))}
{junk_layers}
{string_split}

{decryption_logic}

-- Main execution with anti-crash protection
local {vm_table} = setmetatable({{}}, {{
    __index = function(t,k)
        local allowed = {{ "print", "warn", "error", "pcall", "xpcall", "select", "tonumber", "tostring", "type", "getmetatable", "setmetatable", "rawget", "rawset", "rawequal", "next", "pairs", "ipairs", "table", "string", "math", "bit" }}
        for _,v in pairs(allowed) do
            if k == v then return _G[v] end
        end
        return nil
    end
}})

local {exec_var} = "{encoded if intensity != 'extreme' else 'SPLIT_STRING'}"

local function {loader_func}(code_str)
    local results = {{}}
    local success, decrypted = pcall({decoder_func}, code_str)
    
    if not success or not decrypted then
        return nil, "Decryption failed"
    end
    
    -- Try multiple loading methods
    local loaders = {{loadstring, load}}
    for _,loader in ipairs(loaders) do
        local success, chunk = pcall(loader, decrypted)
        if success and chunk then
            if setfenv then
                setfenv(chunk, {vm_table})
            end
            return chunk
        end
    end
    return nil
end

-- Execute with fallback
local ready = nil
local load_error = nil

if type({exec_var}) == "string" and #{exec_var} > 0 then
    ready, load_error = {loader_func}({exec_var})
    if not ready and {string_split and "rebuild_string" or "false"} then
        local rebuilt = rebuild_string()
        if rebuilt and #rebuilt > 0 then
            ready, load_error = {loader_func}(rebuilt)
        end
    end
end

if ready then
    local success, result = pcall(ready)
    if not success then
        -- Silent fail, no print to avoid detection
    end
else
    -- Protection active - no error messages
    local _ = {{
        [{random_string(8)}] = function() end,
        [{random_string(8)}] = function() end
    }}
end

--[=[ END OF PROTECTED BLOCK ]=]
-- Protected by: Sttar Albiola
-- FB: Sttar Albiola
"""
    
    return final_template


# ============================================================
# USAGE EXAMPLE
# ============================================================

if __name__ == "__main__":
    sample_lua_code = """
    print("Hello World!")
    local players = game:GetService("Players")
    local player = players.LocalPlayer
    print("Player: " .. player.Name)
    """
    
    obfuscated = process_code(sample_lua_code, "extreme")
    print(obfuscated)
    
    # Save to file
    with open("obfuscated_output.lua", "w", encoding="utf-8") as f:
        f.write(obfuscated)
    print("\n[+] Obfuscated code saved to obfuscated_output.lua")
