"use client"
import { SparklesCore } from "@/components/ui/sparkles";
import { HeroParallax } from "@/components/ui/hero-parallax";
import Link from "next/link";
import LogoMark from "@/components/LogoMark";
import { CircularProgress } from '@mui/material';
import { useEffect, useState } from "react";
import NavbarLanding from "@/components/navbarLanding";
import FooterLanding from "@/components/FooterLanding";
import AboutUs from "@/components/AboutUs";

interface Doctor {
  title: string;
  link: string;
  thumbnail: string;
  numberOfReviews: number;
  avarageRating: number;
  id: number;
}

export default function Home() {
  const [doctors, setDoctors] = useState([] as Doctor[]);
  function padArray(docs: Array<Doctor>) {
    if (docs.length === 0) return;
    const originalDocs = [...docs];
    let i = 0;
    while (docs.length < 15) {
      docs.push(originalDocs[i % originalDocs.length]);
      i++;
    }
  }
  const headers = {
    "Content-Type": "application/json"
  };
  async function fetchDoctorList() {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_SERVER_NAME}/doctorList`,
      { headers }
    );
    if (!response.ok) {
      console.log("Error: Request sent no data")
    }
    const data = await response.json();
    padArray(data);
    setDoctors(data);
  }

  useEffect(() => {
    fetchDoctorList();
  }, []);
  return (
    <>
      <NavbarLanding />
      {doctors[0] ? (
        <>
          <main className="w-screen h-lvh">
            <div className="mx-auto h-screen">
              <HeroParallax products={doctors} />
              <AboutUs />
              <div className="h-[40rem] relative w-screen bg-gradient-to-br from-slate-50 to-teal-50 flex flex-col justify-center items-center overflow-hidden">
                <div className="w-screen absolute inset-0 h-screen">
                  <SparklesCore
                    id="tsparticlesfullpage"
                    background="transparent"
                    minSize={0.6}
                    maxSize={1.4}
                    particleDensity={20}
                    className="w-full"
                    particleColor="#5EEAD4"
                  />
                </div>
                <div>
                  <LogoMark size="xl" variant="color" showText className="animate-breathe" />
                </div>
                <div className="flex flex-col sm:flex-row items-center gap-4 mt-6">
                  <Link href="/ContactUs">
                    <button className="px-5 py-2.5 bg-white border border-teal-200 text-teal-700 rounded-lg shadow-sm hover:bg-teal-50 hover:border-teal-300 hover:text-teal-800 hover:-translate-y-0.5 transition-all duration-200 ease-in-out font-medium">
                      Contact Us
                    </button>
                  </Link>
                  <Link href="/Signup">
                    <button className="px-5 py-2.5 bg-white border border-teal-200 text-teal-700 rounded-lg shadow-sm hover:bg-teal-50 hover:border-teal-300 hover:text-teal-800 hover:-translate-y-0.5 transition-all duration-200 ease-in-out font-medium">
                      Sign Up
                    </button>
                  </Link>
                </div>
              </div>
            </div>
          </main>
          <FooterLanding />
        </>
      ) : (
        <div className="w-screen h-screen flex justify-center items-center">
          <CircularProgress color="warning" size={'18rem'} />
        </div>
      )}
    </>
  );
}
