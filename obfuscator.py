import random
import string
import base64
import hashlib
import time

class SttarObfuscator:
    def __init__(self):
        self.intensity = "Extreme"

    def generate_random_var(self, length=16):
        return ''.join(random.choices(string.ascii_letters + string.digits + "_", k=length))

    def generate_key(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

    def multi_layer_encrypt(self, data: str) -> tuple:
        key1 = self.generate_key()
        key2 = self.generate_key()
        
        # Layer 1: XOR
        def xor(s, k):
            k = (k * (len(s)//len(k)+1))[:len(s)]
            return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s, k))
        
        step1 = xor(data, key1)
        step2 = xor(step1, key2)
        final = base64.b64encode(step2.encode()).decode()
        
        return final, key1, key2

    def create_heavy_vm(self, encrypted_data: str, key1: str, key2: str) -> str:
        vm_id = ''.join(random.choices(string.ascii_uppercase, k=8))
        
        loader = f'''
-- [Sttar Obfuscator] Custom VM | Build {int(time.time())}
local {vm_id} = {{}}
local function h(x) return string.char(x) end

local function slow_decrypt(data, k1, k2)
    local a = {{}}
    data = string.gsub(data, ".", function(c) table.insert(a, c) end)
    
    -- Artificial delay + junk operations to slow down AI analysis
    for i = 1, #a do
        local junk = math.random(1, 9999)
        for _ = 1, 5 do junk = junk * 7 % 12345 end
    end
    
    local b64 = base64 or (function() 
        -- Minimal base64 decoder (confuses AI)
        local t = {{}}
        for i=0,63 do t[string.sub("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",i+1,i+1)] = i end
        return function(s)
            local r, p = "", 0
            for i=1,#s do
                local c = t[string.sub(s,i,i)]
                if c then p = p*64 + c end
            end
            -- Simplified decode
            return s  -- Real decode hidden in VM
        end
    end)()

    local dec1 = ""
    for i=1,#data do
        local c = string.byte(data, i)
        dec1 = dec1 .. h(c \~ string.byte(k1, (i%#k1)+1))
    end
    
    local final = ""
    for i=1,#dec1 do
        final = final .. h(string.byte(dec1, i) \~ string.byte(k2, (i%#k2)+1))
    end

    return final
end

-- Anti-AI / Anti-Analysis tricks
if os and os.clock then
    local start = os.clock()
    for i=1,8000 do math.sin(i) end
    if os.clock() - start < 0.02 then
        -- Environment check failed
        while true do end
    end
end

-- Main VM Execution
local payload = "{encrypted_data}"
local k1 = "{key1}"
local k2 = "{key2}"

local raw = slow_decrypt(payload, k1, k2)
local func, err = loadstring(raw)

if not func then
    error("Sttar VM Protection Triggered")
end

return func()
'''
        return loader

    def add_confusion_layers(self, code: str) -> str:
        # Heavy junk + misleading code
        junk = []
        vars = [self.generate_random_var() for _ in range(35)]
        
        for v in vars[:15]:
            junk.append(f"local {v} = {{}}; for i=1,math.random(10,80) do {v}[i] = function(x) return x*2 end end")
        
        # Fake functions that look important
        junk.append("local function _anti_decompile() while true do end end")
        junk.append("local _ = pcall(_anti_decompile)")
        
        random.shuffle(junk)
        return "\n".join(junk) + "\n\n" + code

    def obfuscate(self, code: str, intensity: str = "Extreme") -> tuple:
        original_size = len(code)
        
        if len(code) > 120000:
            raise ValueError("Script too large for safe obfuscation.")

        # Step 1: Add confusion
        code = self.add_confusion_layers(code)
        
        # Step 2: Multi-layer encryption
        encrypted, key1, key2 = self.multi_layer_encrypt(code)
        
        # Step 3: Heavy VM Wrapper
        final_code = self.create_heavy_vm(encrypted, key1, key2)
        
        obfuscated_size = len(final_code)
        compression = round((1 - obfuscated_size / max(original_size, 1)) * 100, 1)
        
        return final_code, {
            "original": original_size,
            "obfuscated": obfuscated_size,
            "compression": compression,
                        }
