// LE BUZZER

const int led1 = 6;
const int led2 = 7;
const int buzzer1 = 8;
const int buzzer2 = 9;
const int button1a = 2;  // Bouton 1 équipe 1
const int button1b = 3;  // Bouton 2 équipe 1
const int button2a = 4;  // Bouton 1 équipe 2
const int button2b = 5;  // Bouton 2 équipe 2

bool equipe1_active = false;
bool equipe2_active = false;

void setup() {
    Serial.begin(9600);  // Initialisation de la communication série

    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(buzzer1, OUTPUT);
    pinMode(buzzer2, OUTPUT);
    pinMode(button1a, INPUT_PULLUP);
    pinMode(button1b, INPUT_PULLUP);
    pinMode(button2a, INPUT_PULLUP);
    pinMode(button2b, INPUT_PULLUP);
}

void loop() {
    if ((digitalRead(button1a) == LOW || digitalRead(button1b) == LOW) && !equipe2_active) {  
        equipe1_active = true;
        Serial.println("Equipe 1"); // Envoi du signal à Python
    }

    if ((digitalRead(button2a) == LOW || digitalRead(button2b) == LOW) && !equipe1_active) {  
        equipe2_active = true;
        Serial.println("Equipe 2"); // Envoi du signal à Python
    }

    if (equipe1_active) {
        digitalWrite(led1, HIGH);
        digitalWrite(buzzer1, HIGH);
    } else {
        digitalWrite(led1, LOW);
        digitalWrite(buzzer1, LOW);
    }

    if (equipe2_active) {
        digitalWrite(led2, HIGH);
        digitalWrite(buzzer2, HIGH);
    } else {
        digitalWrite(led2, LOW);
        digitalWrite(buzzer2, LOW);
    }

    // Réinitialisation lorsque tous les boutons sont relâchés
    if (digitalRead(button1a) == HIGH && digitalRead(button1b) == HIGH &&
        digitalRead(button2a) == HIGH && digitalRead(button2b) == HIGH) {
        equipe1_active = false;
        equipe2_active = false;
    }
}
