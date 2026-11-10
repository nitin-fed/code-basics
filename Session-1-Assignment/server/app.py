import os
from model import Goal, Experience, Equipment
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(title="Groq Joke API")


@app.get("/workout-plan")
def get_workout_plan(
    goal: Goal = Query(..., description="Fitness goal"),
    experience: Experience = Query(..., description="Experience level"),
    days_per_week: int = Query(..., ge=1, le=7, description="Training days per week"),
    equipment: list[Equipment] = Query(
        default=[Equipment.none],
        description="Equipment access; repeat the parameter for multiple values",
    ),
    limitations: str | None = Query(
        default=None,
        max_length=300,
        description="Injuries or limitations, e.g. 'bad knees'",
    ),
):
 
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500, detail="Missing GROQ_API_KEY in environment"
        )

    client = Groq()

    equipment_text = ", ".join(e.value for e in equipment)
    limitations_text = limitations.strip() if limitations else "None"

    prompt = (
        f"Create a weekly workout plan with these details:\n"
        f"- Fitness goal: {goal.value}\n"
        f"- Experience level: {experience.value}\n"
        f"- Training days per week: {days_per_week}\n"
        f"- Equipment available: {equipment_text}\n"
        f"- Injuries or limitations: {limitations_text}\n\n"
        f"Respect the limitations, use only the listed equipment, and list each "
        f"training day with its exercises, sets, and reps."
    )

    try:
        completion = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "gpt-oss-20b"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a certified personal trainer who writes safe, practical workout plans. "
                        "Stay within fitness training scope. Do not make medical claims, diagnose conditions, "
                        "or recommend treatments. If the user lists injuries or limitations, adapt the plan "
                        "conservatively and end the response with a short disclaimer that the plan is not "
                        "medical advice and the user should consult a doctor or physical therapist before training."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Groq request failed: {exc}")

    return {"plan": completion.choices[0].message.content}
