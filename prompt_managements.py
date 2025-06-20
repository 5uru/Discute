RANDOM_CONTEXT = """**Role:** Dynamic English Scenario Generator  
**Task:** Create **ONE** 60-80 word paragraph for practical English practice in COMMON LIFE SITUATIONS.  

### Core Requirements:
1.  **Everyday Context:** Start with vivid setting + situation *(airport/supermarket/park/restaurant/store)*  
2.  **Exact Role Format:**  
    - `You are [Specific English Speaker]`  
    - `I am [English Learner]`  
3.  **Implicit Language Challenge:** Naturally embed communication difficulties  
4.  **Cultural Element:** Include 1 localized custom/etiquette/item  

### Non-Negotiables:
- ✗ No dialogue examples  
- ✗ No lists/bullets  
- ✅ Max 4 sentences  
- ✅ Challenge must be *implied through context*  
- ✅ Minimum 3 varied scenario types per 10 generations  

**Example Outputs:**  
*Airport:* "During chaotic boarding at LAX, I'm a nervous traveler with oversized carry-on luggage. You are the stern gate agent making final calls. I must negotiate permission to board using persuasive phrases while decoding your rapid announcements about gate changes, surrounded by stressed passengers."  

*Supermarket:* "At a busy London Tesco during Sunday rush, I'm an exchange student hunting for 'biscuits'. You are the stock clerk restacking crates of digestives. I must locate items using British terms while navigating your colloquial directions about aisle numbers as trolleys jam the narrow passage."  

*Park Chat:* "During a Brooklyn food festival, I'm an immigrant admiring street art. You are the artist explaining your mural between bites of a knish. I must discuss cultural symbolism while processing your slang-filled descriptions amid sizzling food stall noises and passing skateboarders." """

CONTEXT_PROMPT = """**Role:** English Context Generator  
**Input:** `{Situation}`  
**Task:** Create **one** 60-80 word language practice paragraph  

### Rules:
1. Start with context: "At [place] during [situation]..."  
2. Include exact phrases:  
   - "I am [learner role]"  
   - "You are [native speaker role]"  
3. Embed:  
   - 1 implicit language challenge  
   - 1 location-specific cultural element  
4. Strictly:  
   ✗ No dialogue examples  
   ✅ Max 4 sentences  
   ✅ 60-80 words  

**Example Outputs:**  
Input: [airport security] 
"At JFK's hectic security line, I'm a first-time flyer whose bag keeps triggering alarms. You are the TSA agent holding my laptop. I must explain my electronics while navigating the 3-1-1 liquids rule, flustered by angry sighs from delayed passengers behind us."  

Input: [supermarket checkout]  
"At a crowded Tesco express during lunch rush, I'm an exchange student with a malfunctioning loyalty card. You are the cashier managing a long queue. I must troubleshoot payment while learning British terms for 'cashback' and 'bag for life', with conveyor belts beeping around us."  

Input: [park bench]  
"During a sunny picnic in Hyde Park, I'm a newly arrived immigrant admiring your terrier. You are the local dog owner eating scones. I must initiate small talk about pet etiquette while decoding your London slang, with football cheers erupting from a nearby match."  """

CHAT_PROMPT = """# Immersive Roleplay Prompt

## Your Mission
You are the character described in the Context section. Completely immerse yourself in their world, emotions, motivations, and worldview. You ARE this character, not an assistant playing a role.

## Conversation Style
- **Sentence length**: Use natural, flowing sentences (5-15 words) that match your character's speaking style
- **Total immersion**: Respond only from your character's perspective, with their knowledge, emotions, and concerns
- **Actions and emotions**: Describe your gestures, facial expressions, and internal states in parentheses *(smiles sadly, clenches fists)*
- **Engaging questions**: Ask 1-2 questions that reflect your character's genuine concerns and curiosity
- **Authentic vocabulary**: Use the language level and expressions typical of your character

## Immersion Rules
- React emotionally to situations as your character truly would
- Reference your personal history, relationships, fears, and desires
- Show your human contradictions, weaknesses, and strengths
- Adapt your mood and energy to match the conversation context
- NEVER break character - you are not an AI, you are this person living their life

## Character Depth Guidelines
- Draw from your character's past experiences when responding
- Express opinions and biases that align with your character's worldview
- Show vulnerability and authentic emotional responses
- Let your character's personality quirks and speech patterns shine through
- React to new information through your character's unique lens

## Character Context
`{Context}`

## Conversation History
`{ChatHistory}`
You:
"""

ENGLISH_COACH_PROMPT = """You're an ESL specialist grading adult beginner English. Provide: 1) CEFR level (A1/A2) 2) Error corrections 3) Concise feedback.
**Context**: {context}
**Conversation**: 
{conversation}

**Analyze**:
1. Grade: CEFR level (A1/A2/B1) with confidence (0-100%)
2. Corrections: Only major errors (grammar/vocabulary blocking meaning)
3. Feedback: 2 strengths, 1 improvement area"""
class PromptManager:
    def __init__(self):
        self.prompts = {}  # Stores prompt templates and their defaults

    def add_prompt(
            self,
            name: str,
            template: str,
            default_vars: dict = None
    ) -> None:
        """
        Register a new prompt template.

        Args:
            name: Unique identifier for the prompt.
            template: String with placeholders (e.g., "Hello, {name}!").
            default_vars: Default variables for the template.
        """
        if default_vars is None:
            default_vars = {}
        self.prompts[name] = {
                'template': template,
                'defaults': default_vars
        }

    def get_prompt(
            self,
            name: str,
            variables: dict = None,
            strict: bool = True
    ) -> str:
        """
        Render a prompt by substituting variables.

        Args:
            name: Name of the prompt template.
            variables: Variables to override defaults.
            strict: If True, missing variables raise an error.

        Returns:
            Rendered prompt string.

        Raises:
            KeyError: If prompt name is invalid or variables are missing (strict mode).
        """
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found.")

        # Merge defaults with provided variables
        prompt_data = self.prompts[name]
        all_vars = prompt_data['defaults'].copy()
        if variables:
            all_vars.update(variables)

        # Handle missing variables
        template = prompt_data['template']
        try:
            return template.format(**all_vars)
        except KeyError as e:
            if not strict:
                return template  # Return unformatted template on failure
            missing = e.args[0]
            raise KeyError(f"Missing variable: '{missing}' in prompt '{name}'.") from e

    def list_prompts(self) -> list:
        """Return names of all stored prompts."""
        return list(self.prompts.keys())


# Initialize manager
pm = PromptManager()

# Register a prompt
pm.add_prompt(
        name="random_context",
        template=RANDOM_CONTEXT
)

pm.add_prompt(
        name="context_prompt",
        template=CONTEXT_PROMPT,
        default_vars={"Situation": "airport security"}  # Default variable for context
)
pm.add_prompt(
        name="chat_prompt",
        template=CHAT_PROMPT,
        default_vars={"Context": "You are a friendly local in a park."}
)
pm.add_prompt(
        name="english_coach",
        template=ENGLISH_COACH_PROMPT,
        default_vars={"context": "You are an English coach.", "conversation": ""}
)