import Link from "next/link";
import Image from "next/image";
import { FaPhoneAlt, FaEnvelope, FaClock } from "react-icons/fa";

const NavbarLanding = () => {
    return (
        <header className="w-full flex flex-col z-50 sticky top-0 shadow-md">
            {/* Top Bar - Contact Info */}
            <div className="bg-slate-900 text-gray-300 text-xs sm:text-sm py-2 px-6 md:px-12 lg:px-24 hidden md:flex justify-between items-center">
                <div className="flex gap-6">
                    <div className="flex items-center gap-2 hover:text-orange-400 transition-colors cursor-pointer">
                        <FaPhoneAlt className="text-orange-500" />
                        <span>+1 (555) 123-4567</span>
                    </div>
                    <div className="flex items-center gap-2 hover:text-orange-400 transition-colors cursor-pointer">
                        <FaEnvelope className="text-orange-500" />
                        <span>hello@carecubs.com</span>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <FaClock className="text-orange-500" />
                    <span>Mon - Fri: 8:00 AM - 6:00 PM</span>
                </div>
            </div>

            {/* Main Nav - Links & CTA */}
            <nav className="bg-white w-full h-20 sm:h-24 flex justify-between items-center px-6 md:px-12 lg:px-24">
                {/* Logo */}
                <div className="flex items-center h-full py-2">
                    <Link href="/" className="h-full flex items-center">
                        <Image
                            className="h-12 sm:h-16 w-auto object-contain mix-blend-multiply"
                            src="/logoSmall.png"
                            alt="Care Cubs Logo"
                            width={1080}
                            height={300}
                        />
                    </Link>
                </div>

                {/* Nav Links */}
                <div className="hidden lg:flex items-center gap-8 text-slate-700 font-medium">
                    <Link href="/" className="hover:text-orange-500 transition-colors">Home</Link>
                    <Link href="/#about" className="hover:text-orange-500 transition-colors">About Us</Link>
                    <Link href="/#services" className="hover:text-orange-500 transition-colors">Services</Link>
                    <Link href="/#doctors" className="hover:text-orange-500 transition-colors">Doctors</Link>
                    <Link href="/ContactUs" className="hover:text-orange-500 transition-colors">Contact</Link>
                </div>

                {/* CTA Buttons */}
                <div className="flex items-center gap-3">
                    <Link href="/Login" className="hidden sm:block text-slate-700 font-medium hover:text-orange-500 transition-colors mr-2">
                        Login
                    </Link>
                    <Link href="/Signup">
                        <button className="bg-orange-500 hover:bg-orange-600 text-white font-medium py-2 px-4 rounded-md shadow-md hover:shadow-lg transition-all duration-200 ease-in-out">
                            Book Appointment
                        </button>
                    </Link>
                </div>
            </nav>
        </header>
    );
};

export default NavbarLanding;
