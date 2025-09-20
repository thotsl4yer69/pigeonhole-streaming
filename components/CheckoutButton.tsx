"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertCircle, ArrowRightCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CheckoutButtonProps {
  productId: string;
  productName: string;
}

interface CheckoutResponse {
  status: string;
  reference: string;
  message: string;
  paymentUrl: string;
}

export function CheckoutButton({ productId, productName }: CheckoutButtonProps) {
  const [isProcessing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [receipt, setReceipt] = useState<CheckoutResponse | null>(null);

  async function handleCheckout() {
    setProcessing(true);
    setError(null);
    setReceipt(null);

    try {
      const response = await fetch(`/api/checkout/${productId}`, {
        method: "POST"
      });

      if (!response.ok) {
        throw new Error("Checkout failed");
      }

      const data = (await response.json()) as CheckoutResponse;
      setReceipt(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setProcessing(false);
    }
  }

  return (
    <div className="flex flex-col gap-4" aria-live="polite">
      <Button onClick={handleCheckout} disabled={isProcessing} className="w-full">
        {isProcessing ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> Processing…
          </>
        ) : (
          <>
            Initiate Checkout <ArrowRightCircle className="h-4 w-4" aria-hidden />
          </>
        )}
      </Button>
      <AnimatePresence>
        {receipt ? (
          <motion.div
            key="receipt"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="rounded-2xl border border-cyber-lime/40 bg-black/50 p-4 text-xs text-cyber-teal/80"
          >
            <p className="font-orbitron text-sm uppercase tracking-[0.3em] text-cyber-lime">Signal Locked</p>
            <p className="mt-2 text-white/80">{receipt.message}</p>
            <a
              href={receipt.paymentUrl}
              target="_blank"
              rel="noreferrer"
              className="mt-3 inline-flex items-center gap-2 text-cyber-pink hover:text-white"
            >
              View payment session
              <ArrowRightCircle className="h-4 w-4" aria-hidden />
            </a>
          </motion.div>
        ) : null}
      </AnimatePresence>
      <AnimatePresence>
        {error ? (
          <motion.div
            key="error"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="flex items-start gap-2 rounded-2xl border border-cyber-pink/40 bg-black/50 p-4 text-xs text-cyber-pink"
          >
            <AlertCircle className="mt-[2px] h-4 w-4" aria-hidden />
            <span>
              Unable to launch checkout for {productName}.
              <br />
              <strong>Reason:</strong> {error}
              <br />
              Please try again. If the problem persists, check your connection or contact support.
            </span>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </div>
  );
}
