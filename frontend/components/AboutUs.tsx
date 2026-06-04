import React from 'react';
import { FaHeartbeat, FaUserMd, FaChild, FaEye, FaBullseye } from 'react-icons/fa';

const AboutUs = () => {
  return (
    <section id="about" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Intro Section */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-slate-800 mb-6">
            Welcome to <span className="text-orange-500">Care Cubs</span>
          </h2>
          <p className="text-lg text-slate-600 leading-relaxed">
            At Care Cubs Pediatrics, we believe every child deserves a healthy start. 
            Our state-of-the-art clinic provides a warm, welcoming, and child-friendly environment 
            where expert medical care meets compassionate service. From newborn check-ups to 
            adolescent care, we are here to support your child's journey to a healthy future.
          </p>
        </div>

        {/* Mission & Vision */}
        <div className="grid md:grid-cols-2 gap-10 mb-20">
          <div className="bg-orange-50 rounded-2xl p-8 border border-orange-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-14 h-14 bg-orange-500 text-white rounded-xl flex items-center justify-center mb-6 shadow-lg">
              <FaBullseye className="text-2xl" />
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-4">Our Mission</h3>
            <p className="text-slate-600 leading-relaxed">
              To provide exceptional, evidence-based pediatric care in a nurturing environment. 
              We partner with parents to empower them with knowledge, ensuring the physical, 
              emotional, and developmental well-being of every child we treat.
            </p>
          </div>

          <div className="bg-slate-50 rounded-2xl p-8 border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
            <div className="w-14 h-14 bg-slate-800 text-white rounded-xl flex items-center justify-center mb-6 shadow-lg">
              <FaEye className="text-2xl" />
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-4">Our Vision</h3>
            <p className="text-slate-600 leading-relaxed">
              To be the leading pediatric care provider in the community, recognized for our 
              unwavering commitment to medical excellence, compassionate care, and fostering 
              a healthier, happier future for the next generation.
            </p>
          </div>
        </div>

        {/* Core Values */}
        <div className="text-center mb-12">
          <h3 className="text-3xl font-bold text-slate-800 mb-2">Our Core Values</h3>
          <p className="text-slate-500">The principles that guide everything we do.</p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-6">
            <div className="mx-auto w-16 h-16 bg-orange-100 text-orange-500 rounded-full flex items-center justify-center mb-4">
              <FaHeartbeat className="text-3xl" />
            </div>
            <h4 className="text-xl font-bold text-slate-800 mb-3">Compassion</h4>
            <p className="text-slate-600">
              We treat every child as if they were our own, delivering care with empathy, kindness, and patience.
            </p>
          </div>

          <div className="text-center p-6">
            <div className="mx-auto w-16 h-16 bg-slate-100 text-slate-700 rounded-full flex items-center justify-center mb-4">
              <FaUserMd className="text-3xl" />
            </div>
            <h4 className="text-xl font-bold text-slate-800 mb-3">Excellence</h4>
            <p className="text-slate-600">
              We are dedicated to the highest standards of medical care, continuous learning, and clinical expertise.
            </p>
          </div>

          <div className="text-center p-6">
            <div className="mx-auto w-16 h-16 bg-orange-100 text-orange-500 rounded-full flex items-center justify-center mb-4">
              <FaChild className="text-3xl" />
            </div>
            <h4 className="text-xl font-bold text-slate-800 mb-3">Family-Centered</h4>
            <p className="text-slate-600">
              We believe parents are vital partners in healthcare, fostering open communication and collaborative decisions.
            </p>
          </div>
        </div>

      </div>
    </section>
  );
};

export default AboutUs;
