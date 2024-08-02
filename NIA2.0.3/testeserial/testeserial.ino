#define RESET asm ("jmp (0x0000)")

void setup() {
  // put your setup code here, to run once:
    
  RESET; // onde você quiser no programa e resetar sem problemas.
}

void loop() {
  // put your main code here, to run repeatedly:
  
}
