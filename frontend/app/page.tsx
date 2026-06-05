"use client"
import { HeroParallax } from "@/components/ui/hero-parallax";
import { CircularProgress } from '@mui/material';
import { useEffect, useState } from "react";
import NavbarLanding from "@/components/navbarLanding";
import FooterLanding from "@/components/FooterLanding";
import AboutUs from "@/components/AboutUs";
import ServicesLanding from "@/components/ServicesLanding";
import DoctorsLanding from "@/components/DoctorsLanding";
import Link from "next/link";

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
    const filteredData = data.filter((doc: Doctor) => doc.thumbnail !== "https://i.imgur.com/9g7aq8u.png");
    padArray(filteredData);
    setDoctors(filteredData);
  }

  useEffect(() => {
    fetchDoctorList();
  }, []);
  return (
    <>
      <NavbarLanding />
      {doctors[0] ? (
        <>
          <main className="w-full min-h-screen">
            <div className="mx-auto">
              
              {/* Desktop Parallax Hero */}
              <div className="hidden md:block">
                <HeroParallax products={doctors} />
              </div>

              {/* Mobile Static Hero */}
              <div className="md:hidden bg-gray-100 flex flex-col items-center justify-center py-20 px-6 text-center">
                <h1 className="text-4xl font-bold text-slate-900 mb-4 leading-tight">
                  Your child <br /> Deserves the best
                </h1>
                <p className="text-lg text-slate-600 mb-8 max-w-sm">
                  Our team of highly professional pediatricians will look after your child, so you can be sure your child is in good hands.
                </p>
                <Link href="/Signup">
                  <button className="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white font-semibold py-3 px-8 rounded-full shadow-lg transition-transform hover:scale-105 w-full">
                    Book an Appointment
                  </button>
                </Link>
                
                {/* Mobile showcase images (just show top 2 doctors as preview) */}
                <div className="mt-12 flex flex-col gap-6 w-full max-w-sm">
                  {doctors.slice(0, 2).map((doc, idx) => (
                    <div key={idx} className="relative h-64 w-full rounded-2xl overflow-hidden shadow-md">
                      <img src={doc.thumbnail} alt={doc.title} className="object-cover object-top w-full h-full" />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
                      <h3 className="absolute bottom-4 left-4 text-white font-bold text-xl">{doc.title}</h3>
                    </div>
                  ))}
                </div>
              </div>

              <AboutUs />
              <ServicesLanding />
              <DoctorsLanding doctors={doctors} />
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
