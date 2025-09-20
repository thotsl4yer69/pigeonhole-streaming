import { NextResponse } from "next/server";

export async function POST(_request: Request, { params }: { params: { id: string } }) {
  const reference = crypto.randomUUID();
  const etaMinutes = Math.floor(Math.random() * 20) + 5;

  return NextResponse.json({
    status: "success",
    reference,
    message: `Checkout simulated for device ${params.id}. Expect confirmation in ${etaMinutes} minutes.`,
    paymentUrl: `https://checkout.pigeonhole.dev/mock/${reference}`
  });
}
