import sys

file_path = 'frontend/src/App.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if '{/* 2-Column Dashboard Grid: Recent Cadre Activity & Sovereign Node Telemetry */}' in line:
        line = line.replace('{/* 2-Column Dashboard Grid: Recent Cadre Activity & Sovereign Node Telemetry */}', '{/* 1-Column Dashboard Grid: Recent Cadre Activity */}')
    if 'className="grid grid-cols-1 lg:grid-cols-3 gap-6"' in line:
        line = line.replace('className="grid grid-cols-1 lg:grid-cols-3 gap-6"', 'className="grid grid-cols-1 gap-6"')
    if 'className="lg:col-span-2 space-y-4"' in line:
        line = line.replace('className="lg:col-span-2 space-y-4"', 'className="space-y-4"')
        
    if '{/* Right Column (1/3): Sovereign Node Telemetry */}' in line:
        skip = True
        
    if not skip:
        new_lines.append(line)
        
    # The right column is exactly 1 top-level div with space-y-4.
    # It ends with a </div> before the final closing </div> of the grid.
    # Let's count divs to be safe, or just find the end of the Card.
    if skip and '</div>' in line:
        # Wait, simple parsing is hard.
        pass

# Let's do it with content replace string by string since I can see it exactly in the previous log.
