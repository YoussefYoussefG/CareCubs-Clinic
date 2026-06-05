"use client";
import React, { useState } from "react";
import Link from "next/link";
import LogoMark from "./LogoMark";
import { FaPhoneAlt, FaEnvelope, FaClock, FaBars, FaTimes } from "react-icons/fa";

const NavbarLanding = () => {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
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
            <nav className="bg-slate-900 w-full h-20 sm:h-24 flex justify-between items-center px-6 md:px-12 lg:px-24">
                {/* Logo */}
                <div className="flex items-center h-full py-2">
                    <Link href="/" className="h-full flex items-center hover:opacity-90 transition-opacity">
                        <LogoMark size="md" variant="white" showText />
                    </Link>
                </div>

                {/* Nav Links */}
                <div className="hidden lg:flex items-center gap-8 text-teal-100/70 font-medium">
                    <Link href="/" className="hover:text-teal-300 transition-colors">Home</Link>
                    <Link href="/#about" className="hover:text-teal-300 transition-colors">About Us</Link>
                    <Link href="/#services" className="hover:text-teal-300 transition-colors">Services</Link>
                    <Link href="/#doctors" className="hover:text-teal-300 transition-colors">Doctors</Link>
                    <a href="#contact" className="hover:text-teal-300 transition-colors">Contact</a>
                </div>

                {/* CTA Buttons - Desktop Only */}
                <div className="hidden md:flex items-center gap-3">
                    <Link href="/Login" className="text-teal-100/70 font-medium hover:text-teal-300 transition-colors mr-2">
                        Login
                    </Link>
                    <Link href="/Signup">
                        <button className="bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white font-medium py-2.5 px-5 rounded-lg shadow-lg shadow-teal-500/25 hover:shadow-teal-500/40 hover:-translate-y-0.5 transition-all duration-200 ease-in-out">
                            Book Appointment
                        </button>
                    </Link>
                </div>

                {/* Mobile Menu Toggle */}
                <div className="lg:hidden flex items-center">
                    <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-teal-100/70 hover:text-teal-300 transition-colors">
                        {isMobileMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
                    </button>
                </div>
            </nav>

            {/* Mobile Navigation Drawer */}
            {isMobileMenuOpen && (
                <div className="lg:hidden bg-slate-900 border-t border-slate-800 shadow-lg absolute top-full left-0 w-full z-40">
                    <div className="flex flex-col px-6 py-4 space-y-4 text-teal-100/70 font-medium">
                        <Link href="/" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors border-b border-slate-800 pb-2">Home</Link>
                        <Link href="/#about" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors border-b border-slate-800 pb-2">About Us</Link>
                        <Link href="/#services" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors border-b border-slate-800 pb-2">Services</Link>
                        <Link href="/#doctors" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors border-b border-slate-800 pb-2">Doctors</Link>
                        <a href="#contact" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors border-b border-slate-800 pb-2">Contact</a>
                        <div className="flex flex-col pt-2 space-y-3">
                            <Link href="/Login" onClick={() => setIsMobileMenuOpen(false)} className="hover:text-teal-300 transition-colors">Login</Link>
                            <Link href="/Signup" onClick={() => setIsMobileMenuOpen(false)}>
                                <button className="w-full bg-gradient-to-r from-teal-500 to-emerald-500 text-white font-medium py-2.5 rounded-lg shadow-md transition-all duration-200">
                                    Book Appointment
                                </button>
                            </Link>
                        </div>
                    </div>
                </div>
            )}
        </header>
    );
};

export default NavbarLanding;
