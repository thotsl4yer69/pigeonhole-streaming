import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "relative inline-flex items-center justify-center gap-2 overflow-hidden rounded-md border border-cyber-teal bg-crt-glass px-6 py-3 font-orbitron text-sm uppercase tracking-[0.2em] text-white transition-all duration-200 hover:shadow-neon focus:outline-none focus:ring-2 focus:ring-cyber-teal/80 after:absolute after:inset-0 after:-z-10 after:scale-105 after:bg-gradient-to-r after:from-cyber-pink/20 after:to-cyber-teal/20 after:opacity-0 after:transition-opacity after:duration-500 hover:after:opacity-100",
  {
    variants: {
      variant: {
        default: "bg-gradient-to-r from-cyber-pink/60 via-cyber-teal/50 to-cyber-lime/60",
        ghost: "bg-transparent hover:bg-cyber-teal/10",
        outline: "bg-transparent"
      },
      size: {
        default: "",
        sm: "px-4 py-2 text-xs",
        lg: "px-8 py-4 text-base"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default"
    }
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props}>
        {props.children}
      </Comp>
    );
  }
);
Button.displayName = "Button";

