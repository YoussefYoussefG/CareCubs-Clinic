import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CareCubs Clinic — Pediatric Healthcare",
  description:
    "CareCubs Clinic provides expert pediatric healthcare. Book appointments, manage medical records, and connect with trusted pediatricians online.",
  keywords: [
    "pediatric",
    "clinic",
    "healthcare",
    "children",
    "doctor",
    "appointment",
    "medical records",
    "CareCubs",
  ],
  openGraph: {
    title: "CareCubs Clinic — Pediatric Healthcare",
    description:
      "Expert pediatric healthcare. Book appointments and manage medical records online.",
    type: "website",
    locale: "en_US",
    siteName: "CareCubs Clinic",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans text-slate-800">{children}</body>
    </html>
  );
}