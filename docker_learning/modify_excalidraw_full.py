import json
import random
import string
import os

def gen_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=21))

def create_rectangle(x, y, width, height, stroke_color="#1e1e1e", stroke_width=2, roundness=3, fill_color="transparent"):
    rect_id = gen_id()
    return {
        "id": rect_id,
        "type": "rectangle",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": fill_color,
        "fillStyle": "solid" if fill_color != "transparent" else "hachure",
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": roundness} if roundness else None,
        "seed": random.randint(1, 2000000000),
        "version": 1,
        "versionNonce": random.randint(1, 2000000000),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1780139500000,
        "link": None,
        "locked": False
    }

def create_text(x, y, text, container_id=None, font_size=16, font_family=5, text_align="left", vertical_align="top", stroke_color="#1e1e1e"):
    text_id = gen_id()
    lines = text.split("\n")
    height = len(lines) * font_size * 1.3
    width = max(len(l) for l in lines) * (font_size * 0.58)
    
    return {
        "id": text_id,
        "type": "text",
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": random.randint(1, 2000000000),
        "version": 1,
        "versionNonce": random.randint(1, 2000000000),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1780139500000,
        "link": None,
        "locked": False,
        "text": text,
        "fontSize": font_size,
        "fontFamily": font_family,
        "textAlign": text_align,
        "verticalAlign": vertical_align,
        "containerId": container_id,
        "originalText": text,
        "autoResize": True,
        "lineHeight": 1.3
    }

def create_arrow(start_x, start_y, end_x, end_y, start_elem_id=None, end_elem_id=None, stroke_color="#1e1e1e", stroke_width=2):
    arrow_id = gen_id()
    dx = end_x - start_x
    dy = end_y - start_y
    return {
        "id": arrow_id,
        "type": "arrow",
        "x": start_x,
        "y": start_y,
        "width": max(abs(dx), 1),
        "height": max(abs(dy), 1),
        "angle": 0,
        "strokeColor": stroke_color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": stroke_width,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 2},
        "seed": random.randint(1, 2000000000),
        "version": 1,
        "versionNonce": random.randint(1, 2000000000),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1780139500000,
        "link": None,
        "locked": False,
        "points": [
            [0, 0],
            [dx, dy]
        ],
        "lastCommittedPoint": None,
        "startBinding": {"elementId": start_elem_id, "focus": 0.1, "gap": 5} if start_elem_id else None,
        "endBinding": {"elementId": end_elem_id, "focus": -0.1, "gap": 5} if end_elem_id else None,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "elbowed": False
    }

def main():
    new_elements = []
    
    # -------------------------------------------------------------------------
    # 0. HEADER PANEL (Center Top)
    # -------------------------------------------------------------------------
    header_rect = create_rectangle(-650, -100, 1920, 80, stroke_color="#0066cc", stroke_width=3, fill_color="#e6f2ff")
    header_text = create_text(-400, -80, "🐋 DOCKER INTERACTIVE MASTERCLASS: FROM BLUEPRINT TO MULTI-CONTAINER ORCHESTRATION 🚀", container_id=header_rect["id"], font_size=24, font_family=5, text_align="center", stroke_color="#004080")
    header_rect["boundElements"].append({"id": header_text["id"], "type": "text"})
    new_elements.extend([header_rect, header_text])
    
    # -------------------------------------------------------------------------
    # 1. LEFT PANEL: WHAT IS DOCKER & KEY GLOSSARY TERMS (x=-650 to -250)
    # -------------------------------------------------------------------------
    intro_rect = create_rectangle(-650, 20, 360, 200, stroke_color="#00994c", stroke_width=2, fill_color="#eafaf1")
    intro_title = create_text(-630, 35, "❓ WHAT IS DOCKER?", font_size=18, font_family=5, stroke_color="#006633")
    intro_body = create_text(-630, 70, "Docker is a global engine that packages your\napplication and all its parts (code, database,\ncaches, libraries) into a single, standardized,\nlightweight package called a 'Container'.\n\nAnalogy: Standard Shipping Containers!\nNo matter what is inside, they fit perfectly on\nany container ship, train, or truck in the world.", font_size=13, font_family=5)
    new_elements.extend([intro_rect, intro_title, intro_body])
    
    glossary_rect = create_rectangle(-650, 240, 360, 620, stroke_color="#333333", stroke_width=2, fill_color="#f9f9f9")
    glossary_title = create_text(-630, 255, "📚 KEY DOCKER TERMS FOR BEGINNERS", font_size=18, font_family=5)
    glossary_body = create_text(-630, 290, "📄 DOCKERFILE\nA text file with a step-by-step recipe to build a\ncontainer image. It defines base OS, tools & code.\n\n💿 IMAGE\nAn immutable (read-only) static package containing\neverything needed to run the app. Like a frozen cake.\n\n📦 CONTAINER\nA running, live instance of an image. It is fully isolated\nfrom other containers and runs instantly. Like a baked cake.\n\n📚 REGISTRY (DOCKER HUB)\nA public/private cloud library where developers push\nand pull container images. Like an App Store.\n\n💾 VOLUME\nA persistent hard-drive directory on the host system to\nstore databases and files so data is not lost on crash.\n\n🌐 NETWORK\nPrivate software-defined channels allowing containers\nto talk securely using service name DNS hostnames.", font_size=12, font_family=5)
    new_elements.extend([glossary_rect, glossary_title, glossary_body])

    # -------------------------------------------------------------------------
    # 2. MIDDLE PANEL: SINGLE CONTAINER LIFECYCLE (x=-250 to 250)
    # -------------------------------------------------------------------------
    middle_bg = create_rectangle(-250, 20, 460, 840, stroke_color="#0066cc", stroke_width=2, fill_color="#f2f7fc")
    middle_title = create_text(-230, 35, "🎯 SINGLE-CONTAINER WORKFLOW (STEP-BY-STEP)", font_size=18, font_family=5, stroke_color="#004080")
    new_elements.extend([middle_bg, middle_title])
    
    # Step 1: Write Code (app.py)
    s1_rect = create_rectangle(-210, 80, 380, 80, stroke_color="#1e1e1e", stroke_width=2, fill_color="#ffffff")
    s1_text = create_text(-190, 95, "👉 STEP 1: Write Code (app.py)\nYour basic python file with printing functions.", font_size=14, font_family=5)
    s1_rect["boundElements"].append({"id": s1_text["id"], "type": "text"})
    new_elements.extend([s1_rect, s1_text])
    
    # Step 2: Define Recipe (Dockerfile)
    s2_rect = create_rectangle(-210, 210, 380, 95, stroke_color="#1e1e1e", stroke_width=2, fill_color="#ffffff")
    s2_text = create_text(-190, 220, "👉 STEP 2: Create Blueprint (Dockerfile)\nFROM python:3.11-slim   -> Set base OS\nWORKDIR /app            -> Set internal folder\nCOPY app.py .           -> Copy your code\nCMD ['python', 'app.py']-> Run automatically", font_size=12, font_family=5)
    s2_rect["boundElements"].append({"id": s2_text["id"], "type": "text"})
    new_elements.extend([s2_rect, s2_text])
    
    # Step 3: Build Image
    s3_rect = create_rectangle(-210, 350, 380, 95, stroke_color="#00994c", stroke_width=2, fill_color="#eafaf1")
    s3_text = create_text(-190, 360, "👉 STEP 3: Build the Image Layer-by-Layer\nCommand:\ndocker build -t my-python-app:v1 .\n\nAction: Docker reads Dockerfile, installs python,\ncompiles files, and saves a read-only frozen image.", font_size=12, font_family=5)
    s3_rect["boundElements"].append({"id": s3_text["id"], "type": "text"})
    new_elements.extend([s3_rect, s3_text])
    
    # Step 4: Run Container
    s4_rect = create_rectangle(-210, 490, 380, 95, stroke_color="#ff9900", stroke_width=2, fill_color="#fff9e6")
    s4_text = create_text(-190, 500, "👉 STEP 4: Run the Live Container\nCommand:\ndocker run --name running_app my-python-app:v1\n\nAction: Spawns an isolated sandbox runtime process\nin milliseconds. Writes files inside a thin temp layer.", font_size=12, font_family=5)
    s4_rect["boundElements"].append({"id": s4_text["id"], "type": "text"})
    new_elements.extend([s4_rect, s4_text])
    
    # Step 5: Inject Environment variables
    s5_rect = create_rectangle(-210, 630, 380, 95, stroke_color="#9933ff", stroke_width=2, fill_color="#f9f2ff")
    s5_text = create_text(-190, 640, "👉 STEP 5: Inject Environment Variables at Runtime\nCommand:\ndocker run -e APP_ENV=Production my-python-app:v1\n\nAction: Alters variables dynamically without modifying\nyour source code or building the image again!", font_size=12, font_family=5)
    s5_rect["boundElements"].append({"id": s5_text["id"], "type": "text"})
    new_elements.extend([s5_rect, s5_text])
    
    # Step 6: Registry push/pull
    s6_rect = create_rectangle(-210, 770, 380, 80, stroke_color="#0066cc", stroke_width=2, fill_color="#e6f2ff")
    s6_text = create_text(-190, 780, "👉 STEP 6: Share on Docker Hub / Registry\ndocker push username/my-python-app:v1\ndocker pull username/my-python-app:v1", font_size=13, font_family=5)
    s6_rect["boundElements"].append({"id": s6_text["id"], "type": "text"})
    new_elements.extend([s6_rect, s6_text])
    
    # Connecting middle steps with arrows
    arrow1 = create_arrow(-20, 160, -20, 210, start_elem_id=s1_rect["id"], end_elem_id=s2_rect["id"])
    arrow2 = create_arrow(-20, 305, -20, 350, start_elem_id=s2_rect["id"], end_elem_id=s3_rect["id"])
    arrow3 = create_arrow(-20, 445, -20, 490, start_elem_id=s3_rect["id"], end_elem_id=s4_rect["id"])
    arrow4 = create_arrow(-20, 585, -20, 630, start_elem_id=s4_rect["id"], end_elem_id=s5_rect["id"])
    arrow5 = create_arrow(-20, 725, -20, 770, start_elem_id=s5_rect["id"], end_elem_id=s6_rect["id"])
    new_elements.extend([arrow1, arrow2, arrow3, arrow4, arrow5])

    # -------------------------------------------------------------------------
    # 3. RIGHT PANEL: MULTI-CONTAINER ORCHESTRATION WITH COMPOSE (x=250 to 1250)
    # -------------------------------------------------------------------------
    right_bg = create_rectangle(250, 20, 1020, 840, stroke_color="#ff3399", stroke_width=2, fill_color="#fff2f9")
    right_title = create_text(270, 35, "🎛️ MULTI-CONTAINER ORCHESTRATION (DOCKER COMPOSE)", font_size=18, font_family=5, stroke_color="#cc0066")
    new_elements.extend([right_bg, right_title])
    
    # Compose yaml description
    yaml_rect = create_rectangle(290, 80, 420, 130, stroke_color="#1e1e1e", stroke_width=2, fill_color="#ffffff")
    yaml_text = create_text(305, 95, "📄 docker-compose.yml (Orchestration Script)\nA single YAML file configuring multiple services,\ntheir networks, ports, databases, variables,\nvolumes, and startup dependencies.", font_size=13, font_family=5)
    yaml_rect["boundElements"].append({"id": yaml_text["id"], "type": "text"})
    new_elements.extend([yaml_rect, yaml_text])
    
    # Compose command box
    up_rect = create_rectangle(290, 250, 420, 80, stroke_color="#cc0066", stroke_width=2, fill_color="#ffe6f2")
    up_text = create_text(305, 265, "🚀 COMMAND TO SPIN UP ENTIRE STACK:\ndocker compose up -d\nRuns all containers in background with a single command!", font_size=12, font_family=5)
    up_rect["boundElements"].append({"id": up_text["id"], "type": "text"})
    new_elements.extend([up_rect, up_text])
    
    arrow_yaml_up = create_arrow(500, 210, 500, 250, start_elem_id=yaml_rect["id"], end_elem_id=up_rect["id"])
    new_elements.extend([arrow_yaml_up])
    
    # Visual Services breakdown
    services_border = create_rectangle(750, 80, 480, 540, stroke_color="#333333", stroke_width=2, fill_color="#ffffff")
    services_title = create_text(770, 95, "🐳 RUNTIME SERVICES (DOCKER COMPOSE STACK)", font_size=16, font_family=5)
    new_elements.extend([services_border, services_title])
    
    # Service 1: Python App
    c1_rect = create_rectangle(770, 140, 440, 100, stroke_color="#0066cc", stroke_width=2, fill_color="#e6f2ff")
    c1_text = create_text(785, 155, "🐍 python_app_service (Your Custom Code Container)\n- Runs: my-python-app:v1\n- Port: Published internally to the private virtual network.\n- Tasks: Queries PostgreSQL and caches outputs in Redis.", font_size=12, font_family=5)
    c1_rect["boundElements"].append({"id": c1_text["id"], "type": "text"})
    new_elements.extend([c1_rect, c1_text])
    
    # Service 2: PostgreSQL Database
    c2_rect = create_rectangle(770, 260, 440, 100, stroke_color="#336791", stroke_width=2, fill_color="#ebf2f7")
    c2_text = create_text(785, 275, "🐘 database_sandbox (PostgreSQL 15 Container)\n- Image: postgres:15\n- Port: Maps 5432 on Host machine to 5432 in sandbox container\n- Environment: Set Postgres User, DB, and admin passwords.", font_size=12, font_family=5)
    c2_rect["boundElements"].append({"id": c2_text["id"], "type": "text"})
    new_elements.extend([c2_rect, c2_text])
    
    # Service 3: Redis Cache
    c3_rect = create_rectangle(770, 380, 440, 100, stroke_color="#d82c20", stroke_width=2, fill_color="#fdf0ef")
    c3_text = create_text(785, 395, "🔴 cache_layer (Redis:alpine Cache Container)\n- Image: redis:alpine (Extremely small, 30MB Alpine Linux foot print)\n- Port: Maps 6379 on Host machine to 6379 in cache container\n- Tasks: High-speed temporary RAM database storage.", font_size=12, font_family=5)
    c3_rect["boundElements"].append({"id": c3_text["id"], "type": "text"})
    new_elements.extend([c3_rect, c3_text])
    
    # Private network bar
    net_rect = create_rectangle(770, 500, 440, 100, stroke_color="#9933ff", stroke_width=2, fill_color="#f9f2ff")
    net_text = create_text(785, 515, "🌐 🔒 AUTOMATIC PRIVATE BRIDGE NETWORK\n- Docker Compose creates a private virtual network for these containers\n- Service names act as hostnames! Python App connects to Database via\n  host 'database_sandbox' and to Redis via host 'cache_layer'.", font_size=11, font_family=5)
    net_rect["boundElements"].append({"id": net_text["id"], "type": "text"})
    new_elements.extend([net_rect, net_text])
    
    # Arrows from compose up command to the containers
    arrow_up_c1 = create_arrow(710, 290, 770, 190, start_elem_id=up_rect["id"], end_elem_id=c1_rect["id"])
    arrow_up_c2 = create_arrow(710, 290, 770, 310, start_elem_id=up_rect["id"], end_elem_id=c2_rect["id"])
    arrow_up_c3 = create_arrow(710, 290, 770, 430, start_elem_id=up_rect["id"], end_elem_id=c3_rect["id"])
    new_elements.extend([arrow_up_c1, arrow_up_c2, arrow_up_c3])
    
    # Visual Docker Architecture Layer underneath
    arch_rect = create_rectangle(290, 650, 940, 180, stroke_color="#333333", stroke_width=2, fill_color="#f2f2f2")
    arch_title = create_text(310, 665, "🧱 THE GLOBAL DOCKER RUNTIME ENGINE (HOST OPERATING SYSTEM)", font_size=16, font_family=5)
    arch_body = create_text(310, 700, "1. DOCKER DAEMON (dockerd): Manages all high-level actions, schedules containers, listens to CLI.\n2. CONTAINERS RUNTIME (containerd / runc): Spawns the Linux sandbox environments.\n3. LINUX NAMESPACES: Strict isolation mechanism so containers can't see the host's files or processes.\n4. LINUX CONTROL GROUPS (cgroups): Sets limit caps on hardware (e.g. max memory, CPU cores allocated).\n5. COPY-ON-WRITE: Keeps container base layers clean. Changes are written only to a thin active writable layer.", font_size=12, font_family=5)
    new_elements.extend([arch_rect, arch_title, arch_body])

    # -------------------------------------------------------------------------
    # 4. BOTTOM PANEL: THE DOCKER COMMAND CENTER (x=-650 to 1270, y=890 to 1420)
    # -------------------------------------------------------------------------
    cmd_bg = create_rectangle(-650, 890, 1920, 520, stroke_color="#0066cc", stroke_width=2, fill_color="#f9fcff")
    cmd_title = create_text(-630, 905, "💻 THE DOCKER COMMAND CENTER: SEPARATED BY CATEGORY", font_size=20, font_family=5, stroke_color="#004080")
    new_elements.extend([cmd_bg, cmd_title])
    
    # Col 1: Build Commands (x=-620, width: 440)
    col1_rect = create_rectangle(-620, 950, 440, 430, stroke_color="#00994c", stroke_width=2, fill_color="#ffffff")
    col1_title = create_text(-600, 965, "🛠️ 1. BUILD COMMANDS (Image Creation)", font_size=15, font_family=5, stroke_color="#006633")
    col1_body = create_text(-600, 995, "docker build -t name:tag .\n👉 Build a container image from a Dockerfile.\n\ndocker build --no-cache -t name:tag .\n👉 Forces rebuild of image layers, bypassing cache.\n\ndocker images\n👉 List all container images stored locally on your system.\n\ndocker rmi image_id\n👉 Deletes a local image to free disk space.\n\ndocker tag source_tag target_tag\n👉 Creates an alias tag referencing a target image.\n\ndocker history image_name\n👉 Shows the list of filesystem layers in an image.", font_size=11, font_family=5)
    new_elements.extend([col1_rect, col1_title, col1_body])
    
    # Col 2: Run & Manage Commands (x=-160, width: 460)
    col2_rect = create_rectangle(-160, 950, 460, 430, stroke_color="#ff9900", stroke_width=2, fill_color="#ffffff")
    col2_title = create_text(-140, 965, "🚀 2. RUN & RUNTIME COMMANDS (Execution)", font_size=15, font_family=5, stroke_color="#cc7a00")
    col2_body = create_text(-140, 995, "docker run -d --name name image:tag\n👉 Runs a container in the background (detached mode).\n\ndocker run -p 8080:80 image:tag\n👉 Runs container, mapping Host port 8080 to Container port 80.\n\ndocker run -v /host:/container image:tag\n👉 Runs container, direct-mounting a host folder (bind mount).\n\ndocker run -e MY_VAR=val image:tag\n👉 Injects environment variables dynamically inside container.\n\ndocker ps\n👉 Lists all currently running containers.\n\ndocker ps -a\n👉 Lists all containers (active, stopped, exited, crashed).\n\ndocker stop container_id   /   docker start container_id\n👉 Stops a running container cleanly  /  Starts a stopped container.", font_size=11, font_family=5)
    new_elements.extend([col2_rect, col2_title, col2_body])
    
    # Col 3: Debug & Cleanup Commands (x=320, width: 450)
    col3_rect = create_rectangle(320, 950, 450, 430, stroke_color="#9933ff", stroke_width=2, fill_color="#ffffff")
    col3_title = create_text(340, 965, "🧹 3. DEBUG & SYSTEM CLEANUP COMMANDS", font_size=15, font_family=5, stroke_color="#6600cc")
    col3_body = create_text(340, 995, "docker exec -it container_name sh (or bash)\n👉 SSH / Shell directly into a running container filesystem.\n\ndocker logs -f container_name\n👉 Follows container console logs/stdout output in real-time.\n\ndocker inspect container_name\n👉 Returns comprehensive configuration details in JSON format.\n\ndocker stats\n👉 Live streaming metrics: CPU, Memory, Network & Disk usage.\n\ndocker rm container_id\n👉 Permanently deletes a stopped container.\n\ndocker system prune -a\n👉 CRITICAL CLEANUP: Deletes all stopped containers, unused\n   networks, build caches, and images to free system space.", font_size=11, font_family=5)
    new_elements.extend([col3_rect, col3_title, col3_body])
    
    # Col 4: Compose Commands (x=790, width: 450)
    col4_rect = create_rectangle(790, 950, 450, 430, stroke_color="#ff3399", stroke_width=2, fill_color="#ffffff")
    col4_title = create_text(810, 965, "🎛️ 4. COMPOSE MULTI-CONTAINER COMMANDS", font_size=15, font_family=5, stroke_color="#cc0066")
    col4_body = create_text(810, 995, "docker compose up\n👉 Reads yaml file, downloads layers, starts services in foreground.\n\ndocker compose up -d\n👉 Starts entire multi-container service stack in background.\n\ndocker compose down\n👉 Stops, wipes, and deletes compose containers and networks.\n\ndocker compose ps\n👉 Lists running compose services and their bound ports.\n\ndocker compose logs -f service_name\n👉 Real-time live tails the log output for a specific service.\n\ndocker compose exec service_name sh\n👉 Shell directly inside a service configured in compose yaml.", font_size=11, font_family=5)
    new_elements.extend([col4_rect, col4_title, col4_body])
    
    # Set coordinates and data
    data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://marketplace.visualstudio.com/items?itemName=pomdtr.excalidraw-editor",
        "elements": new_elements,
        "appState": {
            "gridSize": 20,
            "gridStep": 5,
            "gridModeEnabled": False,
            "viewBackgroundColor": "#ffffff"
        },
        "files": {}
    }
    
    filepath = r"d:\kabish_localmodel_exercise\samples\sample.excalidraw"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print("Successfully populated sample.excalidraw with comprehensive educational panels and command center!")

if __name__ == "__main__":
    main()
