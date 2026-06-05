"use client"
import { HeroParallax } from "@/components/ui/hero-parallax";
import { CircularProgress } from '@mui/material';
import { useEffect, useState } from "react";
import NavbarLanding from "@/components/navbarLanding";
import FooterLanding from "@/components/FooterLanding";
import AboutUs from "@/components/AboutUs";
import ServicesLanding from "@/components/ServicesLanding";
import DoctorsLanding from "@/components/DoctorsLanding";

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
              <HeroParallax products={doctors} />
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
