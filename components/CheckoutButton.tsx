"use client";

import { useState, useTransition } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle2, Loader2, TriangleAlert } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CheckoutButtonProps {
  productId: string;
  productName: string;
}

export function CheckoutButton({ productId, productName }: CheckoutButtonProps) {
  const [message, setMessage] = useState<string | null>(null);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [isPending, startTransition] = useTransition();

  const handleCheckout = () => {
    startTransition(async () => {
      try {
        setStatus("idle");
        setMessage(null);
        const response = await fetch(`/api/checkout/${productId}`, {
          method: "POST"
        });

        if (!response.ok) {
          throw new Error("Failed to initiate checkout");
        }

        const payload = (await response.json()) as { reference: string; message: string; paymentUrl: string };
        setStatus("success");
        setMessage(`${payload.message} Reference: ${payload.reference}.`);
        window.open(payload.paymentUrl, "_blank", "noopener,noreferrer");
      } catch (error) {
        console.error(error);
        setStatus("error");
        setMessage("Unable to reach the checkout node. Please retry in a moment.");
      }
    });
  };

  return (
    <div className="space-y-4">
      <Button className="w-full" onClick={handleCheckout} disabled={isPending || status === "success"}>
        {isPending ? (
          <span className="flex items-center gap-2 text-xs uppercase tracking-[0.3em]">
            <Loader2 className="h-4 w-4 animate-spin" />
            Initializing Checkout
          </span>
        ) : (
          <>Initiate Checkout</>
        )}
      </Button>
      <AnimatePresence>
        {message && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
            className="glitch-border flex items-start gap-3 rounded-2xl bg-black/60 p-4 text-xs text-white/80"
          >
            {status === "success" ? (
              <CheckCircle2 className="mt-[2px] h-4 w-4 text-cyber-lime" />
            ) : (
              <TriangleAlert className="mt-[2px] h-4 w-4 text-cyber-pink" />
            )}
            <div>
              <p className="font-orbitron uppercase tracking-[0.3em] text-cyber-teal">{productName}</p>
              <p>{message}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
