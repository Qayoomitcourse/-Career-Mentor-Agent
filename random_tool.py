from agents import function_tool

@function_tool
def get_career_roadmap(field: str) -> str:
    maps = {
        "software engineer": "learn python, DSA Web Dev, Projects ",
        "Data Science": "Master Python, Pandas, ML and real world data set",
        "graphic designer": "Learn Figma, Photoshop, UI/UX, Portfolio",
        "ai": "Study Python, deep learning, Transformer, and AI Tools"
    }
    return maps.get(field.lower(), "No Road Map Found for that field")
