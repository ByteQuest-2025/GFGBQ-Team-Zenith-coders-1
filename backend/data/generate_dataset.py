import pandas as pd
import os

# Training data - 180 samples (30 per category)
TRAIN_DATA = {
    "Utilities": [
        "Street light not working since 3 days",
        "No water supply for entire area",
        "Power cut for more than 8 hours daily",
        "Electricity transformer making sparking noise",
        "Water pipe burst flooding the street badly",
        "Frequent voltage fluctuations damaging appliances",
        "Broadband cable cut not repaired since week",
        "Water pressure very low cannot use properly",
        "Electricity meter reading wrong showing high bill",
        "Water contaminated with dirt and smell bad",
        "Power supply interruption multiple times every day",
        "Street lighting not working entire colony dark",
        "Water motor not working no supply at all",
        "Electric pole tilted dangerous can fall anytime",
        "Drinking water tanker not coming on schedule",
        "Electricity wire hanging low above road dangerous",
        "No water in overhead tank pump not working",
        "Current fluctuation burning our electronic devices",
        "Water quality very poor causing health problems",
        "Street light pole fallen blocking the road",
        "Power backup generator not working during outages",
        "Water connection applied but no response months",
        "Electricity bill calculation wrong need correction",
        "Broadband speed extremely slow not as promised",
        "Water tap installed months ago but no supply",
        "Power cut without notice affecting work from home",
        "Streetlight broken glass dangerous for children",
        "Water leakage from main pipeline wasting water",
        "Electricity connection illegal someone stealing power",
        "Broadband fiber cable damaged hanging on road"
    ],
    "Sanitation": [
        "Garbage not collected for 5 days piling up",
        "Sewage overflow on street smells very terrible",
        "Dustbin overflowing with waste for many days",
        "Drainage blocked water logging everywhere badly",
        "Public toilet extremely dirty and smelly condition",
        "Waste dumping happening near residential area",
        "Open drain full of garbage causing diseases",
        "Septic tank overflow in community area smells",
        "Garbage truck not coming to our area regularly",
        "Stray dogs spreading garbage on roads daily",
        "Manhole overflow sewage water on street",
        "No dustbins provided in crowded market area",
        "Drain water entering houses during heavy rain",
        "Garbage burning creating severe air pollution",
        "Compost pit overflowing with waste terrible smell",
        "Public park full of litter not cleaned regularly",
        "Beach area dirty with plastic waste everywhere",
        "Lake water heavily polluted with sewage discharge",
        "Illegal waste dumping in empty plot daily",
        "Sanitation workers not cleaning streets properly",
        "Garbage segregation not happening at all",
        "Waste collection bins broken and badly damaged",
        "Dead animal carcass not removed for many days",
        "Drain cleaning not done causing severe blockage",
        "Public urination wall needs urgent cleaning",
        "Market area gutters overflowing with dirty water",
        "Composting facility not maintained very smelly",
        "Plastic waste scattered everywhere near school",
        "Drainage system completely choked and blocked",
        "Garbage vehicle always skips our street area"
    ],
    "Safety": [
        "Someone threatening me near bus stand daily",
        "Chain snatching happened yesterday evening here",
        "Harassment by unknown person following me always",
        "Unsafe area no police patrolling at night time",
        "Robbery attempt near ATM center last night",
        "Group creating nuisance and spreading fear",
        "Stalking complaint person following me daily",
        "Drug peddling happening openly in this area",
        "Fighting and violence near liquor shop daily",
        "Woman safety issue eve teasing near college",
        "Theft in house while we were away yesterday",
        "Physical assault happened near park area",
        "Dangerous stray dogs attacking people daily",
        "Fire hazard illegal firecracker storage nearby",
        "Child safety concern suspicious person near school",
        "Domestic violence hearing screams from neighbor house",
        "Bike theft happening very frequently in area",
        "Sexual harassment in public transport daily",
        "Threatening phone calls from unknown numbers",
        "Physical assault by neighbor over small dispute",
        "Burglary attempt last night very scared now",
        "Kidnapping threat to child near home area",
        "Rash driving causing accidents daily high risk",
        "Mob violence during political rally very unsafe",
        "Cyberbullying serious threats on social media",
        "Robbery at weapon point near market yesterday",
        "Arson attempt fire started deliberately last night",
        "Extortion threat demanding money or violence",
        "Murder threat received need urgent police protection",
        "Hit and run accident person critically injured"
    ],
    "Health": [
        "Hospital staff very rude not treating properly",
        "No doctor available in primary health center",
        "Medicine out of stock in government hospital",
        "Dengue cases increasing need fogging urgently",
        "Food poisoning from street vendor near school",
        "Hospital beds not available patients on floor",
        "Vaccination drive not happening in our area",
        "Contaminated water causing diseases in locality",
        "Hospital equipment not working properly very old",
        "Long waiting time many hours to see doctor",
        "Ambulance service not responding to emergency calls",
        "Health worker not visiting for antenatal checkup",
        "Epidemic outbreak fever cases rising need help",
        "Expired medicines being given at government clinic",
        "Very unhygienic conditions in government hospital",
        "Mental health facility not available in district",
        "Blood bank shortage urgent need blood donation",
        "Malaria risk mosquito breeding near stagnant water",
        "Hospital refused emergency treatment demanding money",
        "Child immunization schedule not followed properly",
        "TB patient not getting free medicines anymore",
        "Health insurance claim rejected without proper reason",
        "Rabies risk from stray dog bite no vaccine",
        "Hospital negligence patient condition badly worsened",
        "Covid testing facility not available here locally",
        "Maternity ward conditions very poor and unhygienic",
        "Disabled accessibility issues in hospital building",
        "Pharmacy selling fake counterfeit medicines illegally",
        "Health checkup camp cancelled without any notice",
        "Oxygen cylinder shortage in hospital very critical"
    ],
    "Administrative": [
        "Birth certificate not issued for 2 months delay",
        "Ration card application pending for very long time",
        "Property tax payment receipt not received yet",
        "Driving license renewal delayed no response at all",
        "Passport application stuck at police verification stage",
        "Pension not credited for last 3 months delay",
        "Voter ID card correction not processed at all",
        "Building plan approval taking too much long time",
        "Aadhaar card address change request still pending",
        "Income certificate application rejected without reason",
        "Land record correction not updated for many years",
        "Marriage certificate not issued even after fees paid",
        "Death certificate delayed causing many problems",
        "Trade license renewal application completely ignored",
        "Caste certificate verification taking many months",
        "RTI application reply not received within time",
        "Grievance filed online but no response from office",
        "Corruption staff demanding bribe for normal service",
        "Office staff absent during office hours no service",
        "Online portal not working cannot submit application",
        "Document verification process delayed indefinitely",
        "Pension card not issued to eligible senior citizen",
        "Property mutation application stuck for many years",
        "Disability certificate application rejected unfairly",
        "Scholarship amount not credited to bank account",
        "BPL card application pending for 6 months now",
        "Electricity bill payment not reflecting in system",
        "Water connection duplicate bill being charged wrongly",
        "Refund not processed even after multiple requests",
        "Office timing very inconvenient for working people"
    ],
    "Infrastructure": [
        "Road full of dangerous potholes causing accidents",
        "Bridge damaged badly needs urgent repair work",
        "Traffic signal not working at main junction",
        "Footpath completely broken near school area",
        "Big pothole on main road causing accidents daily",
        "Road construction incomplete for many months now",
        "Manhole cover missing on busy main road",
        "Pedestrian crossing marking completely faded invisible",
        "Road surface caved in after recent heavy rain",
        "Traffic light timing not synchronized causing jams",
        "Broken footpath very dangerous for elderly people",
        "No street lights in entire new colony area",
        "Road safety barriers fallen creating severe hazard",
        "Speed breakers too high damaging all vehicles",
        "Drainage metal grill missing on main road",
        "Public park main gate broken not closing properly",
        "Bus shelter roof completely collapsed needs fixing",
        "Road divider badly damaged at multiple places",
        "Zebra crossing paint completely worn out invisible",
        "Highway guardrail broken damaged after accident",
        "Bicycle lane obstructed by illegally parked vehicles",
        "Public toilet facility has broken door locks",
        "Footbridge stairs badly damaged and very slippery",
        "Road direction sign boards fallen not visible",
        "Pavement stones loose everywhere causing tripping",
        "Street name board completely missing causing confusion",
        "Public bench in park area badly broken",
        "Road lane marking completely faded very dangerous",
        "Pedestrian subway flooded with rainwater always",
        "Flyover expansion joint damaged making loud noise"
    ]
}

# Generate training CSV
train_rows = []
for category, texts in TRAIN_DATA.items():
    for text in texts:
        train_rows.append({"text": text, "category": category})

train_df = pd.DataFrame(train_rows)
train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
os.makedirs("data", exist_ok=True)
train_df.to_csv("data/complaints_train.csv", index=False)
print(f"✅ Generated {len(train_df)} training samples")
print(f"📊 Category distribution:\n{train_df['category'].value_counts()}")

# Generate test data (30 samples - 5 per category)
TEST_DATA = {
    "Infrastructure": [
        "Main road has very deep dangerous pothole",
        "Street lamp completely broken dark at night",
        "Bridge needs urgent repair work unsafe now",
        "Traffic signal malfunction causing many accidents",
        "Footpath badly damaged people tripping daily"
    ],
    "Sanitation": [
        "Garbage pile near house not collected at all",
        "Drain completely blocked dirty water everywhere",
        "Public toilet facility very dirty needs cleaning",
        "Sewage smell absolutely unbearable in entire area",
        "Waste bins overflowing for many days now"
    ],
    "Utilities": [
        "No electricity since morning all work stopped",
        "Water supply very irregular and low pressure",
        "Wifi internet not working need urgent fix",
        "Power transmission line fallen on road dangerous",
        "Water quality very bad causing illness problems"
    ],
    "Safety": [
        "Theft attempt happened last night very scared",
        "Harassment complaint near bus stop need help",
        "Very dangerous area no security presence at all",
        "Fighting happened causing injuries need police now",
        "Child safety serious risk suspicious activity here"
    ],
    "Health": [
        "Doctor not available this is emergency situation",
        "Hospital staff negligent patient badly suffering",
        "Medicine shortage crisis at health center",
        "Disease outbreak spreading need immediate action",
        "Ambulance delayed very long patient critical condition"
    ],
    "Administrative": [
        "Certificate application pending for many months",
        "Document verification process extremely delayed",
        "Application rejected without proper reason given",
        "Government office not responding to queries",
        "Service delayed staff demanding illegal bribe"
    ]
}

test_rows = []
for category, texts in TEST_DATA.items():
    for text in texts:
        test_rows.append({"text": text, "category": category})

test_df = pd.DataFrame(test_rows)
test_df.to_csv("data/complaints_test.csv", index=False)
print(f"✅ Generated {len(test_df)} test samples")
