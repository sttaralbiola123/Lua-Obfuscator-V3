import random
import string
import base64
import time

class SttarObfuscator:
    def __init__(self):
        self.intensity = "Extreme"

    def generate_random_var(self, length=18):
        return ''.join(random.choices(string.ascii_letters + string.digits + "_", k=length))

    def generate_key(self, length=48):
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+", k=length))

    def multi_xor_encrypt(self, data: str) -> tuple:
        key1 = self.generate_key()
        key2 = self.generate_key()
        key3 = self.generate_key(32)  # Third layer

        def xor(s, k):
            k = (k * (len(s) // len(k) + 1))[:len(s)]
            return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, k))

        step1 = xor(data, key1)
        step2 = xor(step1, key2)
        step3 = xor(step2, key3)
        final = base64.b64encode(step3.encode('utf-8')).decode('utf-8')
        
        return final, key1, key2, key3

    def create_ultra_vm(self, encrypted_data: str, key1: str, key2: str, key3: str) -> str:
        vm_name = ''.join(random.choices(string.ascii_uppercase, k=10))
        junk_vars = [self.generate_random_var() for _ in range(45)]

        vm = f'''
-- Sttar Obfuscator Ultra VM | Build {int(time.time())}
local {vm_name} = {{}}
local function h(x) return string.char(x) end

-- === HEAVY JUNK LAYER ===
{"".join([f"local {v} = {{}}; for i=1,math.random(15,65) do {v}[i] = function(x) return x * {random.randint(2,9)} end end\n" for v in junk_vars[:25]])}

local function decrypt_layer3(data, k1, k2, k3)
    local result = {{}}
    local len = #data
    
    -- Layer 1
    for i = 1, len do
        local byte = string.byte(data, i)
        local k = string.byte(k1, ((i-1) % #k1) + 1)
        result[i] = h(byte \~ k)
    end
    local s1 = table.concat(result)
    
    -- Layer 2
    local result2 = {{}}
    for i = 1, #s1 do
        local byte = string.byte(s1, i)
        local k = string.byte(k2, ((i-1) % #k2) + 1)
        result2[i] = h(byte \~ k)
    end
    local s2 = table.concat(result2)
    
    -- Layer 3
    local result3 = {{}}
    for i = 1, #s2 do
        local byte = string.byte(s2, i)
        local k = string.byte(k3, ((i-1) % #k3) + 1)
        result3[i] = h(byte \~ k)
    end
    
    return table.concat(result3)
end

-- Anti-Analysis & Executor Safety
if getgenv then getgenv().SttarProtected = true end
if syn and syn.cache then syn.cache_clear() end

-- Runtime delay + confusion
local start_time = tick()
for i = 1, 12000 do
    local _ = math.sin(i) * math.random()
end
if tick() - start_time < 0.001 then
    -- Fake infinite loop trap (never triggers on real executors)
end

local payload = "{encrypted_data}"
local k1 = "{key1}"
local k2 = "{key2}"
local k3 = "{key3}"

local success, raw_code = pcall(decrypt_layer3, payload, k1, k2, k3)

if not success or not raw_code then
    error("Sttar VM Protection: Decryption Failed")
end

-- Final Execution
local func, load_err = loadstring(raw_code)
if not func then
    error("Sttar VM: Loadstring Failed - " .. (load_err or "Unknown"))
end

return func()
'''
        return vm

    def add_string_splitting(self, code: str) -> str:
        # Split strings to confuse static analysis
        def split_string(s):
            if len(s) < 8:
                return f'"{s}"'
            parts = [s[i:i+random.randint(3,7)] for i in range(0, len(s), random.randint(3,7))]
            return "..".join(f'"{p}"' for p in parts)
        
        # Simple replacement for common strings (can be expanded)
        return code

    def obfuscate(self, code: str, intensity: str = "Extreme") -> tuple:
        original_size = len(code)
        
        if len(code) > 130000:
            raise ValueError("Script too large (max \~130k chars)")

        # Layer 1: Junk + Confusion
        junk_code = "\n".join([f"local {self.generate_random_var()} = function() end" for _ in range(35)])
        code = junk_code + "\n\n" + self.add_string_splitting(code)

        # Layer 2: Triple XOR + Base64
        encrypted, key1, key2, key3 = self.multi_xor_encrypt(code)

        # Layer 3: Ultra VM
        final_code = self.create_ultra_vm(encrypted, key1, key2, key3)

        obfuscated_size = len(final_code)
        compression = round((1 - obfuscated_size / max(original_size, 1)) * 100, 1)

        return final_code, {
            "original": original_size,
            "obfuscated": obfuscated_size,
            "compression": compression,
            }
