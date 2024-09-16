import math

def binary_entropy(p: float) -> float:
    """Calculate the binary entropy function H(p)."""
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def channel_capacity(p: float) -> float:
    """Calculate the channel capacity C of the Binary Symmetric Channel."""
    return 1 - binary_entropy(p)

def explain_binary_entropy(p: float) -> str:
    """Provide an explanation for the binary entropy H(p)."""
    if p == 0 or p == 1:
        return f"The binary entropy function H(p) is 0 because the uncertainty is minimal. When p = {p}, the outcome is certain."
    
    entropy = binary_entropy(p)
    explanation = (f"The binary entropy function H(p) measures the amount of uncertainty or randomness associated with the probability p.\n"
                   f"For p = {p}, H(p) is calculated as follows:\n"
                   f"H(p) = -p * log2(p) - (1-p) * log2(1-p)\n"
                   f"Substituting p = {p}:\n"
                   f"H(p) = -({p}) * log2({p}) - (1 - {p}) * log2(1 - {p})\n"
                   f"The entropy value H(p) is: {entropy:.4f}")
    return explanation

def explain_channel_capacity(p: float) -> str:
    """Provide an explanation for the channel capacity C."""
    capacity = channel_capacity(p)
    explanation = (f"The channel capacity C is the maximum rate at which information can be transmitted reliably.\n"
                   f"It is calculated as:\n"
                   f"C = 1 - H(p)\n"
                   f"Where H(p) is the binary entropy function.\n"
                   f"With a flip probability p = {p}, the capacity C is: {capacity:.4f}\n"
                   f"When p is close to 0 or 1, the capacity is close to 1 bit per channel use, meaning the channel is almost perfect.\n"
                   f"When p is 0.5, the capacity is 0 because the channel is fully noisy and no reliable information can be transmitted.")
    return explanation

def main():
    print("Welcome to the Binary Symmetric Channel (BSC) Capacity Calculator!")
    
    while True:
        try:
            p = float(input("Enter the probability of a bit being flipped (between 0 and 1): "))
            if p < 0 or p > 1:
                print("Please enter a probability between 0 and 1.")
                continue
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            continue
        
        print(f"\nFor a Binary Symmetric Channel with flip probability p = {p}:")
        
        # Calculate and explain binary entropy
        entropy = binary_entropy(p)
        print(f"- The binary entropy H(p) is: {entropy:.4f}")
        print(explain_binary_entropy(p))
        
        # Calculate and explain channel capacity
        capacity = channel_capacity(p)
        print(f"- The channel capacity C is: {capacity:.4f}")
        print(explain_channel_capacity(p))
        
        # Ask if the user wants to calculate again
        again = input("\nWould you like to calculate again? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Thank you for using the BSC Capacity Calculator!")
            break

if __name__ == "__main__":
    main()
