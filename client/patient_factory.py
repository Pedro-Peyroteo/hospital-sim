from faker import Faker
import random

from symptom_severity import RED_SYMPTOMS, YELLOW_SYMPTOMS, GREEN_SYMPTOMS, ALL_SYMPTOMS

# Initializes Faker object.
fake = Faker()

# Load once at a module level.
SYMPTOMS_LIST = ALL_SYMPTOMS

# Defines patient urgency for probabilistic distribution.
# Returns list of symptom/s with probability considered.
def urgency_for_symptom(symptom: str) -> str:
    if symptom in RED_SYMPTOMS:
        return random.choices(["RED", "YELLOW"], weights=[0.8, 0.2])[0]
    elif symptom in YELLOW_SYMPTOMS:
        return random.choices(["YELLOW", "GREEN"], weights=[0.6, 0.4])[0]
    elif symptom in GREEN_SYMPTOMS:
        return random.choices(["GREEN", "YELLOW"], weights=[0.8, 0.2])[0]
    else:
        return random.choice(["GREEN", "YELLOW", "RED"])  # Fallback

    
# Generates a patient's metadata with help of Faker library.
def generate_patient(pid: int) -> dict:
    num_symptoms = random.randint(1, 3)  # 1 to 3 symptoms
    symptoms = random.sample(SYMPTOMS_LIST, k=num_symptoms)
    
    return {
        "patient_id": pid,
        "name": fake.name(),
        "age": random.randint(18, 90),
        "gender": random.choice(["Male", "Female", "Other"]),
        "address": fake.address().replace("\n", ", "),
        "blood_type": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
        "insurance": random.choice(["Private", "Public", "None"]),
        "language": fake.language_name(),
        "symptoms": ",".join(symptoms)  # CSV string
    }