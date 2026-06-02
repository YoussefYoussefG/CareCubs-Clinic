import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

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
      <body className={inter.className}>{children}</body>
    </html>
  );
}