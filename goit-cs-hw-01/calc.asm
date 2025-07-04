org  0x100                   ; Indicate this is a .COM program (starts at offset 0x100)

section .data
    a db 5                   ; Define variable a = 5
    b db 3                   ; Define variable b = 3
    c db 2                   ; Define variable c = 2
    resultMsg db 'Result: $' ; Message before showing the result (must end with $ for DOS)

section .text
_start:
    ; Perform calculation: b - c + a
    mov al, [b]              ; Load value of b into AL
    sub al, [c]              ; Subtract c => AL = b - c
    add al, [a]              ; Add a => AL = b - c + a

    ; Convert result (a number) to ASCII character (only works for single-digit results)
    add al, 30h              ; Convert to ASCII by adding 48 (0x30)

    ; Print message "Result: "
    mov ah, 09h              ; DOS function to print string
    lea dx, resultMsg        ; Load address of the message into DX
    int 21h                  ; Call interrupt to print the string

    ; Print the result (ASCII character in AL → move to DL for output)
    mov dl, al               ; Move result to DL
    mov ah, 02h              ; DOS function to print single character
    int 21h                  ; Call interrupt to print character

    ; Exit the program
    mov ax, 4C00h            ; DOS function to terminate program
    int 21h