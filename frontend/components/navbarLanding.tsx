import Link from "next/link";
import LogoMark from "./LogoMark";
import { FaPhoneAlt, FaEnvelope, FaClock } from "react-icons/fa";

const NavbarLanding = () => {
    return (
        <header className="w-full flex flex-col z-50 sticky top-0 shadow-md font-sans">
            {/* Top Bar - Contact Info */}
            <div className="bg-gradient-to-r from-slate-900 to-teal-950 text-teal-50 text-xs sm:text-sm py-2 px-6 md:px-12 lg:px-24 hidden md:flex justify-between items-center">
                <div className="flex gap-6">
                    <div className="flex items-center gap-2 hover:text-teal-300 transition-colors cursor-pointer">
                        <FaPhoneAlt className="text-teal-400" />
                        <span>+1 (555) 123-4567</span>
                    </div>
                    <div className="flex items-center gap-2 hover:text-teal-300 transition-colors cursor-pointer">
                        <FaEnvelope className="text-teal-400" />
                        <span>hello@carecubs.com</span>
                    </div>
                </div>
                <div className="flex items-center gap-2 text-teal-100">
                    <FaClock className="text-teal-400" />
                    <span>Mon - Fri: 8:00 AM - 6:00 PM</span>
                </div>
            </div>

            {/* Main Nav - Links & CTA */}
            <nav className="bg-white w-full h-20 sm:h-24 flex justify-between items-center px-6 md:px-12 lg:px-24">
                {/* Logo */}
                <div className="flex items-center h-full py-2">
                    <Link href="/" className="h-full flex items-center hover:opacity-90 transition-opacity">
                        <LogoMark size="md" variant="color" showText />
                    </Link>
                </div>

                {/* Nav Links */}
                <div className="hidden lg:flex items-center gap-8 text-slate-700 font-medium">
                    <Link href="/" className="hover:text-teal-600 transition-colors">Home</Link>
                    <Link href="/#about" className="hover:text-teal-600 transition-colors">About Us</Link>
                    <Link href="/#services" className="hover:text-teal-600 transition-colors">Services</Link>
                    <Link href="/#doctors" className="hover:text-teal-600 transition-colors">Doctors</Link>
                    <Link href="/ContactUs" className="hover:text-teal-600 transition-colors">Contact</Link>
                </div>

                {/* CTA Buttons */}
                <div className="flex items-center gap-3">
                    <Link href="/Login" className="hidden sm:block text-slate-700 font-medium hover:text-teal-600 transition-colors mr-2">
                        Login
                    </Link>
                    <Link href="/Signup">
                        <button className="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white font-medium py-2.5 px-5 rounded-lg shadow-lg shadow-teal-500/25 hover:shadow-teal-500/40 hover:-translate-y-0.5 transition-all duration-200 ease-in-out">
                            Book Appointment
                        </button>
                    </Link>
                </div>
            </nav>
        </header>
    );
};

export default NavbarLanding;
