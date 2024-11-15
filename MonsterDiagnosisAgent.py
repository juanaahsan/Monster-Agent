class MonsterDiagnosisAgent:
    def __init__(self):
        pass

    def solve(self, diseases, patient_symptoms):
        from collections import defaultdict

        # Identify the vitamins that are abnormal in the patient's symptoms
        target_vitamins = {vitamin for vitamin, level in patient_symptoms.items() if level != "0"}

        # Filter diseases that affect any of the target vitamins
        relevant_diseases = {}
        for disease_name, vitamin_effects in diseases.items():
            if any(vitamin_effects[vitamin] != "0" for vitamin in target_vitamins):
                relevant_diseases[disease_name] = vitamin_effects

        disease_names = list(relevant_diseases.keys())

        # Precompute the effects of each disease on the target vitamins
        disease_effects = {}
        for disease_name, vitamin_effects in relevant_diseases.items():
            effects = {}
            for vitamin in target_vitamins:
                effect = vitamin_effects[vitamin]
                if effect == "+":
                    effects[vitamin] = 1
                elif effect == "-":
                    effects[vitamin] = -1
                else:
                    effects[vitamin] = 0
            disease_effects[disease_name] = effects

        max_possible_effects = {vitamin: 0 for vitamin in target_vitamins}
        min_possible_effects = {vitamin: 0 for vitamin in target_vitamins}
        for vitamin in target_vitamins:
            for disease_name in disease_names:
                effect = disease_effects[disease_name][vitamin]
                if effect > 0:
                    max_possible_effects[vitamin] += effect
                elif effect < 0:
                    min_possible_effects[vitamin] += effect


        self.best_solution = None
        self.best_solution_size = float('inf')

        for max_diseases in range(1, len(disease_names) + 1):
            self.search(
                current_diseases=[],
                index=0,
                max_diseases=max_diseases,
                disease_names=disease_names,
                disease_effects=disease_effects,
                patient_symptoms=patient_symptoms,
                target_vitamins=target_vitamins,
                current_effects={},
                max_possible_effects=max_possible_effects,
                min_possible_effects=min_possible_effects
            )
            if self.best_solution:
                break  

        return self.best_solution if self.best_solution else []

    def search(self, current_diseases, index, max_diseases, disease_names, disease_effects, patient_symptoms, target_vitamins, current_effects, max_possible_effects, min_possible_effects):

        if len(current_diseases) >= self.best_solution_size:
            return

        if self.matches_symptoms(current_effects, patient_symptoms, target_vitamins):
            self.best_solution = current_diseases.copy()
            self.best_solution_size = len(current_diseases)
            return

        if index >= len(disease_names) or len(current_diseases) >= max_diseases:
            return

        disease_name = disease_names[index]


        new_effects = current_effects.copy()
        for vitamin in target_vitamins:
            effect = disease_effects[disease_name][vitamin]
            new_effects[vitamin] = new_effects.get(vitamin, 0) + effect


        if self.is_promising(new_effects, patient_symptoms, target_vitamins, disease_names[index + 1:], disease_effects):
            current_diseases.append(disease_name)
            self.search(
                current_diseases=current_diseases,
                index=index + 1,
                max_diseases=max_diseases,
                disease_names=disease_names,
                disease_effects=disease_effects,
                patient_symptoms=patient_symptoms,
                target_vitamins=target_vitamins,
                current_effects=new_effects,
                max_possible_effects=max_possible_effects,
                min_possible_effects=min_possible_effects
            )
            current_diseases.pop()

        self.search(
            current_diseases=current_diseases,
            index=index + 1,
            max_diseases=max_diseases,
            disease_names=disease_names,
            disease_effects=disease_effects,
            patient_symptoms=patient_symptoms,
            target_vitamins=target_vitamins,
            current_effects=current_effects,
            max_possible_effects=max_possible_effects,
            min_possible_effects=min_possible_effects
        )

    def matches_symptoms(self, current_effects, patient_symptoms, target_vitamins):
        for vitamin in target_vitamins:
            net_effect = current_effects.get(vitamin, 0)
            symptom = patient_symptoms[vitamin]
            if symptom == "+" and net_effect <= 0:
                return False
            if symptom == "-" and net_effect >= 0:
                return False
            if symptom == "0" and net_effect != 0:
                return False
        return True

    def is_promising(self, current_effects, patient_symptoms, target_vitamins, remaining_diseases, disease_effects):
        for vitamin in target_vitamins:
            net_effect = current_effects.get(vitamin, 0)
            symptom = patient_symptoms[vitamin]
            max_possible = net_effect
            min_possible = net_effect
            for disease_name in remaining_diseases:
                effect = disease_effects[disease_name][vitamin]
                if effect > 0:
                    max_possible += effect
                elif effect < 0:
                    min_possible += effect
            if symptom == "+" and max_possible <= 0:
                return False  
            if symptom == "-" and min_possible >= 0:
                return False  
            if symptom == "0" and net_effect != 0 and ((net_effect > 0 and min_possible > 0) or (net_effect < 0 and max_possible < 0)):
                return False 
        return True
