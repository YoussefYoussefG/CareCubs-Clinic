import React from 'react';
import Image from 'next/image';
import { formatFullName } from '@/utils/formatFuncs';

interface Doctor {
  title: string;
  link: string;
  thumbnail: string;
  numberOfReviews: number;
  avarageRating: number;
  id: number;
  bio?: string;
}

const DoctorsLanding = ({ doctors }: { doctors: Doctor[] }) => {
  // Filter out any padded doctors if they are duplicates, or just show unique doctors
  // Since padding was used for parallax, we want to only show unique doctors here
  const uniqueDoctors = Array.from(new Map(doctors.map(doc => [doc.id, doc])).values());

  if (!uniqueDoctors || uniqueDoctors.length === 0) return null;

  return (
    <section id="doctors" className="py-24 bg-slate-50">
      <div className="max-w-7xl mx-auto px-6 md:px-12 lg:px-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-slate-900 mb-4">Meet Our Doctors</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Our team of experienced and caring pediatricians are dedicated to providing the highest quality healthcare for your children.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
          {uniqueDoctors.map((doctor) => (
            <div 
              key={doctor.id} 
              className="bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 border border-slate-100 flex flex-col group"
            >
              <div className="relative h-72 w-full overflow-hidden bg-slate-200">
                <Image
                  src={doctor.thumbnail}
                  alt={doctor.title}
                  fill
                  className="object-cover object-top group-hover:scale-105 transition-transform duration-500"
                />
              </div>
              <div className="p-8 flex flex-col flex-grow">
                <h3 className="text-2xl font-bold text-slate-800 mb-1">{formatFullName(doctor.title)}</h3>
                <div className="flex items-center gap-1 mb-4 text-orange-400">
                  <span className="text-sm font-semibold text-slate-600 mr-2">
                    {doctor.avarageRating > 0 ? `${doctor.avarageRating} ★` : 'New'}
                  </span>
                  <span className="text-xs text-slate-400">
                    ({doctor.numberOfReviews} reviews)
                  </span>
                </div>
                <p className="text-slate-600 leading-relaxed text-sm flex-grow">
                  {doctor.bio || "Expert pediatrician dedicated to providing compassionate and comprehensive care for your child's health and well-being."}
                </p>
                <div className="mt-6 pt-6 border-t border-slate-100">
                  <a 
                    href="/Signup" 
                    className="inline-flex items-center justify-center w-full py-3 px-6 bg-teal-50 text-teal-700 font-semibold rounded-xl hover:bg-teal-500 hover:text-white transition-colors duration-300"
                  >
                    Book Appointment
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default DoctorsLanding;
