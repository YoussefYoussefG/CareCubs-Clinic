import React from 'react';
import { FaStethoscope, FaSyringe, FaBaby, FaHeartbeat } from 'react-icons/fa';

const services = [
  {
    title: "General Checkups",
    description: "Comprehensive physical exams to ensure your child's healthy growth and development at every stage.",
    icon: <FaStethoscope className="text-3xl text-teal-500" />
  },
  {
    title: "Vaccinations",
    description: "Safe and timely immunizations to protect your little ones from preventable diseases.",
    icon: <FaSyringe className="text-3xl text-teal-500" />
  },
  {
    title: "Newborn Care",
    description: "Specialized care and guidance for your newborn's crucial first months of life.",
    icon: <FaBaby className="text-3xl text-teal-500" />
  },
  {
    title: "Emergency Care",
    description: "Prompt, expert medical attention for sudden illnesses or minor pediatric emergencies.",
    icon: <FaHeartbeat className="text-3xl text-teal-500" />
  }
];

const ServicesLanding = () => {
  return (
    <section id="services" className="py-16 md:py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6 md:px-12 lg:px-24">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-5xl font-bold text-slate-900 mb-4">Our Services</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            We offer a comprehensive range of pediatric services tailored to meet the unique healthcare needs of your growing child.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {services.map((service, index) => (
            <div 
              key={index} 
              className="bg-slate-50 p-8 rounded-2xl shadow-sm hover:shadow-md hover:-translate-y-1 transition-all duration-300 border border-slate-100 flex flex-col items-center text-center group"
            >
              <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mb-6 group-hover:bg-teal-200 transition-colors">
                {service.icon}
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">{service.title}</h3>
              <p className="text-slate-600 leading-relaxed text-sm">
                {service.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default ServicesLanding;
