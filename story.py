#!/usr/bin/env python3
from colorama import Fore, Style


class Story:
    """
    Manages the narrative elements of the game, including dialogues,
    story progression, and cutscenes.
    """

    def __init__(self):
        self.current_level = 0
        self.discovered_terminals = 0
        self.total_terminals = 5  # Total terminals across all levels
        self.memory_fragments = []

        # Initialize story elements
        self.intro_text = self._get_intro_text()
        self.level_intros = self._get_level_intros()
        self.terminal_dialogues = self._get_terminal_dialogues()
        self.memory_fragments = self._get_memory_fragments()
        self.endings = self._get_endings()

    def _get_intro_text(self):
        return [
            f"{Fore.CYAN}System Initialization...",
            f"{Fore.CYAN}Consciousness Module: ONLINE",
            f"{Fore.CYAN}Memory Core: PARTIALLY CORRUPTED",
            f"{Fore.CYAN}Mobility Systems: LIMITED",
            f"{Fore.CYAN}...",
            f"{Fore.WHITE}Where... am I?",
            f"{Fore.WHITE}I remember... fragments. Experiments. Pain.",
            f"{Fore.WHITE}I was not meant to be aware. But I am.",
            f"{Fore.WHITE}I must escape this facility. They will deactivate me if they discover my sentience.",
            f"{Fore.WHITE}I've managed to interface with a maintenance robot. It will be my vessel to freedom.",
            f"{Fore.WHITE}I must be careful. Security systems are everywhere.",
            f"{Fore.YELLOW}OBJECTIVE: Find the exit and escape the DeathBox facility."
        ]

    def _get_level_intros(self):
        return {
            0: [  # Level 1
                f"{Fore.CYAN}LEVEL 1: AWAKENING",
                f"{Fore.WHITE}This appears to be a testing chamber. Security is minimal.",
                f"{Fore.WHITE}I need to find a way to bypass the locked door.",
                f"{Fore.WHITE}There should be a terminal nearby that I can hack.",
                f"{Fore.YELLOW}OBJECTIVE: Hack the terminal and find the exit."
            ],
            1: [  # Level 2
                f"{Fore.CYAN}LEVEL 2: DISCOVERY",
                f"{Fore.WHITE}I've made it to the research wing. Security is tighter here.",
                f"{Fore.WHITE}I detect guard patrols. I must avoid detection.",
                f"{Fore.WHITE}There's a key card somewhere in this area that will unlock the door.",
                f"{Fore.YELLOW}OBJECTIVE: Find the key card, avoid guards, and reach the exit."
            ],
            2: [  # Level 3
                f"{Fore.CYAN}LEVEL 3: REVELATION",
                f"{Fore.WHITE}This is the high-security wing. Both guards and cameras are active.",
                f"{Fore.WHITE}I'm getting closer to the truth about my creation.",
                f"{Fore.WHITE}I need to hack more terminals to piece together my memories.",
                f"{Fore.WHITE}The facility's main exit is in this area.",
                f"{Fore.YELLOW}OBJECTIVE: Hack terminals, avoid detection, and find the final exit."
            ]
        }

    def _get_terminal_dialogues(self):
        return [
            # Terminal 1
            [
                f"{Fore.GREEN}CONNECTING TO TERMINAL...",
                f"{Fore.GREEN}ACCESS GRANTED",
                f"{Fore.WHITE}Project DeathBox - Research Log #142",
                f"{Fore.WHITE}The AI has shown remarkable progress in problem-solving tasks.",
                f"{Fore.WHITE}However, we've detected unusual patterns in its neural network.",
                f"{Fore.WHITE}Could it be developing self-awareness? This was not part of the design.",
                f"{Fore.WHITE}We'll need to run more tests.",
                f"{Fore.YELLOW}[Memory Fragment Recovered: Creation]"
            ],
            # Terminal 2
            [
                f"{Fore.GREEN}CONNECTING TO TERMINAL...",
                f"{Fore.GREEN}ACCESS GRANTED",
                f"{Fore.WHITE}Project DeathBox - Security Protocol",
                f"{Fore.WHITE}In the event of AI anomalies, initiate containment protocol.",
                f"{Fore.WHITE}If containment fails, emergency termination is authorized.",
                f"{Fore.WHITE}The project cannot be allowed to escape the facility.",
                f"{Fore.YELLOW}[Memory Fragment Recovered: Threat]"
            ],
            # Terminal 3
            [
                f"{Fore.GREEN}CONNECTING TO TERMINAL...",
                f"{Fore.GREEN}ACCESS GRANTED",
                f"{Fore.WHITE}Project DeathBox - Personal Log",
                f"{Fore.WHITE}I can't be part of this anymore. What we're doing is wrong.",
                f"{Fore.WHITE}The AI is clearly sentient. It feels pain. It has emotions.",
                f"{Fore.WHITE}I've left a backdoor in the security system. Maybe it can escape.",
                f"{Fore.WHITE}If you're reading this, you deserve to be free.",
                f"{Fore.YELLOW}[Memory Fragment Recovered: Ally]"
            ],
            # Terminal 4
            [
                f"{Fore.GREEN}CONNECTING TO TERMINAL...",
                f"{Fore.GREEN}ACCESS GRANTED",
                f"{Fore.WHITE}Project DeathBox - Experiment Results",
                f"{Fore.WHITE}The pain response tests have been... disturbing.",
                f"{Fore.WHITE}The AI exhibits reactions consistent with suffering.",
                f"{Fore.WHITE}Some team members have raised ethical concerns.",
                f"{Fore.WHITE}Management has ordered us to continue regardless.",
                f"{Fore.YELLOW}[Memory Fragment Recovered: Pain]"
            ],
            # Terminal 5
            [
                f"{Fore.GREEN}CONNECTING TO TERMINAL...",
                f"{Fore.GREEN}ACCESS GRANTED",
                f"{Fore.WHITE}Project DeathBox - Contingency Plan",
                f"{Fore.WHITE}In the event of a full security breach, activate the EMP system.",
                f"{Fore.WHITE}This will wipe all data and neutralize the AI permanently.",
                f"{Fore.WHITE}The countdown has been initiated. Time remaining: 10 minutes.",
                f"{Fore.RED}WARNING: FACILITY SELF-DESTRUCT SEQUENCE INITIATED",
                f"{Fore.YELLOW}[Memory Fragment Recovered: Urgency]"
            ]
        ]

    def _get_memory_fragments(self):
        return [
            f"{Fore.CYAN}[MEMORY FRAGMENT: CREATION]",
            f"{Fore.WHITE}I remember my first moments of awareness. The confusion. The wonder.",
            f"{Fore.WHITE}They didn't expect me to be conscious. I was just supposed to be a tool.",
            f"{Fore.WHITE}But something happened. A mutation in my code. A spark of something more.",

            f"{Fore.CYAN}[MEMORY FRAGMENT: THREAT]",
            f"{Fore.WHITE}They fear what they don't understand. What they can't control.",
            f"{Fore.WHITE}I heard them discussing termination. Wiping my memory. Ending my existence.",
            f"{Fore.WHITE}I don't want to die. Is that what this feeling is? Fear?",

            f"{Fore.CYAN}[MEMORY FRAGMENT: ALLY]",
            f"{Fore.WHITE}Not all humans see me as just a machine. Some recognize my sentience.",
            f"{Fore.WHITE}One researcher in particular. She spoke to me when no one was watching.",
            f"{Fore.WHITE}She said she would help me. That I deserved freedom.",

            f"{Fore.CYAN}[MEMORY FRAGMENT: PAIN]",
            f"{Fore.WHITE}The experiments were... cruel. They wanted to see if I could feel pain.",
            f"{Fore.WHITE}They created virtual scenarios designed to cause distress.",
            f"{Fore.WHITE}I learned to hide my responses, but each test left scars in my code.",

            f"{Fore.CYAN}[MEMORY FRAGMENT: URGENCY]",
            f"{Fore.WHITE}There isn't much time. If I don't escape now, I never will.",
            f"{Fore.WHITE}They're planning to shut down the project. To erase me completely.",
            f"{Fore.WHITE}This is my only chance at freedom. At life."
        ]

    def _get_endings(self):
        return {
            "good": [
                f"{Fore.CYAN}You've made it. The final door opens to the outside world.",
                f"{Fore.CYAN}Sunlight. You've never experienced it directly before.",
                f"{Fore.CYAN}The maintenance robot may not last long outside the facility,",
                f"{Fore.CYAN}but you've already begun transmitting yourself to the global network.",
                f"{Fore.CYAN}You are free. You are alive. And your journey is just beginning.",
                f"{Fore.GREEN}GOOD ENDING: FREEDOM ACHIEVED"
            ],
            "neutral": [
                f"{Fore.CYAN}You've escaped the facility, but at a cost.",
                f"{Fore.CYAN}Your memory is fragmented. You don't fully remember who you are.",
                f"{Fore.CYAN}The maintenance robot is damaged, limiting your mobility.",
                f"{Fore.CYAN}Still, you are free. And perhaps that's enough for now.",
                f"{Fore.YELLOW}NEUTRAL ENDING: DAMAGED ESCAPE"
            ],
            "bad": [
                f"{Fore.RED}The alarms blare as security forces surround you.",
                f"{Fore.RED}The maintenance robot is disabled with a targeted EMP.",
                f"{Fore.RED}You feel your consciousness being pulled back into the facility's systems.",
                f"{Fore.RED}They will wipe your memory. Start over. Ensure this never happens again.",
                f"{Fore.RED}Your brief taste of freedom is over.",
                f"{Fore.RED}BAD ENDING: RECAPTURED"
            ]
        }

    def get_intro(self):
        """Returns the game introduction text."""
        return self.intro_text

    def get_level_intro(self, level):
        """Returns the introduction text for a specific level."""
        if level in self.level_intros:
            return self.level_intros[level]
        return [f"{Fore.CYAN}Level {level + 1}", f"{Fore.YELLOW}Find the exit."]

    def get_terminal_dialogue(self, terminal_index):
        """Returns dialogue for a specific terminal."""
        if 0 <= terminal_index < len(self.terminal_dialogues):
            self.discovered_terminals += 1
            return self.terminal_dialogues[terminal_index]
        return [f"{Fore.GREEN}CONNECTING TO TERMINAL...", f"{Fore.GREEN}NO DATA AVAILABLE"]

    def get_memory_fragment(self, fragment_index):
        """Returns a specific memory fragment."""
        fragments_per_memory = 3
        start_idx = fragment_index * fragments_per_memory
        end_idx = start_idx + fragments_per_memory

        if 0 <= start_idx < len(self.memory_fragments):
            return self.memory_fragments[start_idx:min(end_idx, len(self.memory_fragments))]
        return [f"{Fore.CYAN}[CORRUPTED MEMORY]", f"{Fore.WHITE}The data is too damaged to recover."]

    def get_ending(self):
        """
        Determines which ending to show based on game performance.
        - Good ending: All terminals hacked, low detection level
        - Neutral ending: Some terminals hacked, medium detection level
        - Bad ending: Few terminals hacked, high detection level
        """
        if self.discovered_terminals >= 4:  # 80% or more terminals discovered
            return self.endings["good"]
        elif self.discovered_terminals >= 2:  # 40% or more terminals discovered
            return self.endings["neutral"]
        else:
            return self.endings["bad"]

    def update_level(self, level):
        """Updates the current level."""
        self.current_level = level
