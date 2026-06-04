import random
import base64
import zlib
import time
import hashlib

def random_string(length=12):
    """Generate a confusing string with similar-looking characters."""
    chars = ['i', 'l', 'I', '1', '0', 'O', 'o', '|', '/', '\\', '_', '-', '~']
    start_char = random.choice(['i', 'l', 'I', 'o', 'O', 'x', 'y', 'z'])
    return start_char + "".join(random.choice(chars) for _ in range(length - 1))

def random_number(min_val=100, max_val=9999):
    return random.randint(min_val, max_val)

def hex_encode_string(source_str: str) -> str:
    """Convert string to Lua hex escape sequence (\\xXX)."""
    return "".join(f"\\x{ord(c):02x}" for c in source_str)

def double_encode(source_str: str) -> str:
    """Base64 then hex encoding."""
    b64 = base64.b64encode(source_str.encode()).decode()
    return hex_encode_string(b64)

def triple_encode(source_str: str) -> str:
    """zlib compress → base64 → hex."""
    compressed = zlib.compress(source_str.encode())
    b64 = base64.b64encode(compressed).decode()
    return hex_encode_string(b64)

def generate_signature(source_code: str) -> str:
    """Create a SHA256 signature of the original code."""
    return hashlib.sha256(source_code.encode()).hexdigest()[:32]

def generate_fake_functions(count=15) -> str:
    """Decoy functions that look real but do nothing."""
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
    """Split a long hex string into shuffled chunks."""
    chunks = []
    chunk_size = random.randint(15, 40)
    for i in range(0, len(hex_string), chunk_size):
        chunks.append(f'"{hex_string[i:i+chunk_size]}"')
    random.shuffle(chunks)
    original_order = list(range(len(chunks)))
    random.shuffle(original_order)
    reverse_map = {original_order[i]: i for i in range(len(original_order))}
    split_code = f"""
local function rebuild_string()
    local parts = {{ {", ".join(chunks)} }}
    local result = ""
    local order = {{ {', '.join(str(reverse_map[i]) for i in range(len(chunks)))} }}
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
    """Advanced anti‑analysis layer."""
    var1 = random_string(8)
    var2 = random_string(10)
    var3 = random_string(6)
    var4 = random_string(12)
    return f"""
--[=[ ANTI-AI / ANTI-ANALYSIS LAYER ]=]
local {var1} = {{
    pcall(function() return debug and debug.getinfo end),
    pcall(function() return rawget(_G, "getfenv") end),
    pcall(function() return rawget(_G, "setfenv") end),
    pcall(function() return rawget(_G, "loadstring") end)
}}
local {var2} = debug and debug.traceback or function() return "" end
if type({var2}) == "function" and #{var2}() > 100 then
    local _ = {var2}(nil, {random_number(1,10)})
end
local {var3} = {{
    ["_"] = function(x) return not not x end,
    ["__"] = function(x) return not x end
}}
local {var4} = 0
for i=1,{random_number(50,200)} do
    {var4} = {var4} + i
    if {var4} > {random_number(1000,5000)} then
        {var4} = {var4} % {random_number(100,999)}
    end
end
if {var4} == 0 then
    local _ = {{}}
    for _=1,{random_number(100,500)} do
        table.insert(_, string.char({random_number(65,90)}))
    end
end
"""

def generate_anti_tamper() -> str:
    """Basic tamper detection."""
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
local {random_string(10)} = (function()
    local _, chunk = pcall(function() 
        return debug and debug.getinfo(1, "S") 
    end)
    return chunk and chunk.source or "unknown"
end)()
if type({random_string(10)}) == "string" and #{random_string(10)} > 10 then
    -- integrity placeholder
else
    error("[STTAR] Code integrity check failed")
end
"""

def generate_control_flow_obfuscation() -> str:
    """Junk control flow to confuse decompilers."""
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

def generate_metadata_obfuscation() -> str:
    """Hide strings behind metatables."""
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
local {random_string(8)} = (function()
    local chars = {{}}
    for i=1,{random_number(50,100)} do
        chars[i] = string.char({random_number(65,122)})
    end
    return table.concat(chars):sub({random_number(5,20)}, {random_number(30,50)})
end)()
"""

def process_code(source_code: str, intensity: str = "extreme") -> str:
    """
    Main obfuscation entry point.
    Returns a fully obfuscated Lua script.
    """
    if not source_code.strip():
        raise ValueError("Input code is empty!")
    if len(source_code) > 150000:
        raise ValueError("Source code too large (max 150k characters).")

    # Choose encoding depth based on intensity
    if intensity == "extreme":
        encoded = triple_encode(source_code)
        encoding_type = "TRIPLE_LAYERED + ANTI-AI"
    elif intensity == "medium":
        encoded = double_encode(source_code)
        encoding_type = "DOUBLE_LAYERED"
    else:
        encoded = hex_encode_string(source_code)
        encoding_type = "SINGLE_LAYERED"

    signature = generate_signature(source_code)

    # Build junk layers
    junk_layers = ""
    for _ in range(random.randint(5, 15)):
        j_var = random_string(random.randint(10, 18))
        junk_layers += f"local {j_var} = {{ {random_number()}, {random_number()}, {random_number()} }};\n"
        junk_layers += f"table.sort({j_var}, function(a,b) return a > b end);\n"
        junk_layers += f"for i=1,#{j_var} do {j_var}[i] = {j_var}[i] + {random_number(1,50)} end\n"

    string_split = generate_string_splitting(encoded) if intensity == "extreme" else ""

    decryption_logic = f"""
local function {random_string(12)}(data)
    if type(data) ~= "string" then return nil end
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

{generate_anti_ai_detection()}
{generate_anti_tamper()}
{generate_control_flow_obfuscation()}
{generate_metadata_obfuscation()}
{generate_fake_functions(random.randint(10,20))}
{junk_layers}
{string_split}
{decryption_logic}

local load_function = loadstring or load
if not load_function then
    error("This environment does not support dynamic code loading.")
end

local encoded_str = "{encoded if intensity != 'extreme' else 'SPLIT_STRING'}"
local final_code = encoded_str
if encoded_str == "SPLIT_STRING" and rebuild_string then
    final_code = rebuild_string()
end

local success, chunk = pcall(function()
    local decrypted = {random_string(12)}(final_code)
    return load_function(decrypted)
end)

if success and chunk then
    pcall(chunk)
end
--[=[ END OF PROTECTED BLOCK ]=]
-- Protected by: Sttar Albiola
-- FB: Sttar Albiola
"""
    return final_template
```
