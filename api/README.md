# SeizureSavvy Database Schema

## Tables
The database schema includes the following tables:

- `users`: Stores user information, including username and password hash.
- `prodromes`: Stores information about prodromes, such as name and description.
- `user_prodromes`: Associates prodromes with user logs and stores intensity levels.
- `auras`: Stores information about auras, including name and description.
- `user_auras`: Associates auras with user logs and indicates their presence.
- `triggers`: Stores trigger information, including name and description.
- `user_triggers`: Associates triggers with user logs and includes any notes.
- `seizure_types`: Stores information about seizure types, such as name and description.
- `seizure_episodes`: Stores details about seizure episodes, including duration, frequency, and postictal symptoms.
- `user_logs`: Tracks user activity logs and timestamps.


## Variables

### Prodromes

The prodromal phase usually starts a few hours or even days before the actual seizure.

| Variable | Measurement | Explanation |
| --- | --- | --- |
| headache | a scale of 0 to 10, with 10 being most intense |  |
| numbness or tingling | a scale of 0 to 10, with 10 being most intense |  |
| tremor | a scale of 0 to 10, with 10 being most intense | It is shaking or trembling movements in one or more parts of the body, most commonly affecting a person's hands. It can also occur in the arms, legs, head, vocal cords, and torso. |
| dizziness | a scale of 0 to 10, with 10 being most intense |  |
| feeling lightheaded | a scale of 0 to 10, with 10 being most intense |  |
| nausea | a scale of 0 to 10, with 10 being most intense |  |
| anxiety | a scale of 0 to 10, with 10 being most intense |  |
| Mood changes | a scale of 0 to 10, with 10 being most intense | irritability, anger,..etc |
| Insomnia | a scale of 0 to 10, with 10 being most intense | Difficulty falling asleep |
| Difficulty focusing | a scale of 0 to 10, with 10 being most intense |  |

### Auras

Auras immediately (within minutes) precede a developing seizure 

| Variable | Measurement | Explanation |
| --- | --- | --- |
| Visual Disturbances | Binary | Vision difficulties,  colored or flashing lights, or hallucinations (seeing something that isn’t actually there). |
| Hearing sounds | Binary | Ear ringing or buzzing, or sound hallucinations |
| unusual smell or taste | Binary |  |
| a ‘rising’ feeling in the stomach | Binary |  |
| déjà vu | Binary | feeling like you’ve ‘been here before’) |
| Jamais vu | Binary | a feeling that you’re seeing something you know well for the first time |
| sudden intense feeling of fear or joy | Binary |  |
| a strange feeling like a ‘wave’ going through the head | Binary |  |
| stiffness or twitching in part of the body | Binary |  |
| a feeling of numbness or tingling | Binary |  |
| a sensation that an arm or leg feels bigger or smaller than it actually is | Binary |  |
| Confusion | Binary |  |


### Triggers

| Variable | Measurement | Explanation |
| --- | --- | --- |
| sleep deprivation |  |  |
| stress |  |  |
| alcohol |  |  |
| drugs |  |  |
| missing a meal |  |  |
| fevers |  |  |
| physical exertion |  |  |
| flashing light |  |  |
| skipping a seizure medication dose |  |  |
| Monthly periods |  |  |


### Episodes

| Variable | Measurement | Description |
| --- | --- | --- |
| Number of Episodes | Discrete values (1, 2, 3,..) | Number of episodes the person had on that given day. For each episode, the patient needs to input the following variables. |
| Type of Seizure | Categorical (the user selects a general category and then a subcategory): Focal [Focal aware (Partial), Focal Impaired Awareness (Complex partial), Focal to Bilateral Tonic-Clonic, Unknown], Generalized [Absence Seizures, Tonic-Clonic Seizures, Tonic Seizures, Clonic Seizures, Myoclonic Seizures, Atonic Seizures (Drop attacks)], Complex, Unknown | Types are focal (originating in one part of the brain) or generalized (involving both sides of the brain). This requires the user to be aware of the type of seizures they have through information provided by the doctor. Sometimes, it is unknown. The type of seizure can vary per episode for a single patient, a phenomenon known as seizure heterogeneity. This variability is particularly noted in individuals diagnosed with epilepsy. Please check the notes below for definitions.  |
| Duration (for each episode) | in minutes; unknown must be an option) | The length of the seizure episode can provide insights into its severity and necessary interventions. |
| Frequency (for each episode) | Discrete values (1, 2, 3,..); unknown must be an option | How many back-to-back episodes the patient had during a single episode? Episodes can sometimes look like a few episodes back-to-back with a gap in the middle which can be a period of consciousness or unconsciousness but without shaking,..etc. I expect most answers to be 1.  |
| Emergency Intervention | Boolean | Whether or not it required emergency intervention  |
| Postictal Headache | duration in mins and intensity on a 0-10 scale | Documenting symptoms experienced after the seizure (e.g., confusion, fatigue, headache) can provide insights into the seizure's impact and recovery time. |
| Postictal Confusion | duration in mins and intensity on a 0-10 scale | |
| Postictal Fatigue | duration in mins and intensity on a 0-10 scale | |

#### Types of Seizures

##### Focal Seizures (aka partial seizures)

Focal seizures start in one area of the brain. They are subdivided based on the level of awareness during the seizure:

1. **Focal Aware Seizures** (aka simple partial seizures):
    - The person remains conscious and aware during the seizure. Symptoms can include twitching, sensory changes like tingling, or emotional changes.
2. **Focal Impaired Awareness Seizures** (aka complex partial seizures):
    - The person's consciousness is impaired or altered. May involve repetitive, non-purposeful movements, such as lip-smacking, fidgeting, or walking in circles.
3. **Focal to Bilateral Tonic-Clonic Seizures**:
    - Starts in one part of the brain as a focal seizure but then spreads to both sides, becoming a generalized seizure. Symptoms start focal and then progress to the tonic-clonic movements associated with generalized seizures.

##### Generalized Seizures

Generalized seizures involve all areas of the brain from the onset. They are classified into several types, each with distinct features:

1. **Absence Seizures** (previously known as petit mal seizures):
    - Characterized by brief, sudden lapses in attention or staring spells. May occur several times a day and often go unnoticed.
2. **Tonic-Clonic Seizures** (previously known as grand mal seizures):
    - The most recognized type, characterized by a sudden loss of consciousness, body stiffening (tonic phase), and shaking (clonic phase). May involve biting the tongue, urinary incontinence, and can lead to significant fatigue after the episode.
3. **Tonic Seizures**:
    - Involve sudden stiffening of the muscles, often leading to a fall. Typically occur in clusters, mostly during sleep.
4. **Clonic Seizures**:
    - Characterized by repeated, jerky muscle movements on both sides of the body.
5. **Myoclonic Seizures**:
    - Brief, shock-like jerks of a muscle or a group of muscles. The person is usually awake and able to think clearly.
6. **Atonic Seizures** (also known as drop attacks):
    - A sudden loss of muscle tone leads to collapsing or dropping down, often resulting in falls and injuries.

##### Complex and Special Syndromes

Some epilepsy syndromes involve both focal and generalized seizures, and their classification may depend on the age of onset, the types of seizures experienced, and EEG findings. Examples include Dravet syndrome, Lennox-Gastaut syndrome, and Juvenile Myoclonic Epilepsy.

### Medications

| Variable | Measurement | Description |
| --- | --- | --- |
| Dosage |  |  |
| Medication |  |  |
|  |  |  |


## References
