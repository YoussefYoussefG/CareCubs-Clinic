import Link from "next/link";
import { FaPhoneAlt, FaEnvelope, FaMapMarkerAlt, FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn } from "react-icons/fa";
import LogoMark from "./LogoMark";

const FooterLanding = () => {
    return (
        <footer id="contact" className="relative bg-slate-900 text-gray-300 overflow-hidden font-sans">
            {/* Animated Heartbeat Top Border */}
            <div className="absolute top-0 left-0 w-full h-1">
                <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 1440 4" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path 
                        d="M0 2H300L320 2L330 -10L350 20L360 2H1080L1100 2L1110 -10L1130 20L1140 2H1440" 
                        stroke="#5EEAD4" 
                        strokeWidth="2"
                        strokeDasharray="1440"
                        strokeDashoffset="0"
                        className="animate-heartbeat drop-shadow-[0_0_8px_rgba(94,234,212,0.8)]"
                    />
                </svg>
            </div>

            {/* Background Gradient & Floating Orbs */}
            <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-teal-950/40 to-slate-900 pointer-events-none">
                <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-teal-500/10 rounded-full blur-3xl animate-float-orb"></div>
                <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl animate-float-orb" style={{ animationDelay: '2s' }}></div>
            </div>

            <div className="relative pt-20 pb-10 px-6 md:px-12 lg:px-24 z-10 max-w-7xl mx-auto">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
                    {/* Column 1: Brand */}
                    <div className="flex flex-col gap-6">
                        <Link href="/" className="inline-block hover:opacity-90 transition-opacity">
                            <LogoMark size="md" variant="white" showText />
                        </Link>
                        <p className="text-sm leading-relaxed text-teal-100/70 font-light">
                            Compassionate care for growing smiles. We provide expert pediatric medical services in a warm, welcoming environment.
                        </p>
                    </div>

                    {/* Column 2: Quick Links */}
                    <div className="flex flex-col gap-5">
                        <h3 className="text-white text-lg font-semibold tracking-wide">Quick Links</h3>
                        <div className="flex flex-col gap-3 text-sm font-medium">
                            {['Home', 'About Us', 'Services', 'Our Doctors', 'Patient Portal'].map((link) => (
                                <Link 
                                    key={link}
                                    href={link === 'Home' ? '/' : link === 'Patient Portal' ? '/Login' : `/#${link.toLowerCase().replace(' our', '').replace(' ', '')}`}
                                    className="group relative inline-flex w-fit text-teal-100/70 hover:text-teal-300 transition-colors"
                                >
                                    <span>{link}</span>
                                    <span className="absolute -bottom-1 left-0 w-full h-[1px] bg-teal-400 origin-left scale-x-0 group-hover:scale-x-100 transition-transform duration-300 ease-out"></span>
                                </Link>
                            ))}
                        </div>
                    </div>

                    {/* Column 3: Contact Info */}
                    <div className="flex flex-col gap-5">
                        <h3 className="text-white text-lg font-semibold tracking-wide">Contact Us</h3>
                        <div className="flex flex-col gap-4 text-sm text-teal-100/70">
                            <div className="flex items-start gap-3 group">
                                <div className="mt-1 p-2 rounded-lg bg-teal-900/50 text-teal-400 group-hover:bg-teal-500 group-hover:text-white transition-colors">
                                    <FaMapMarkerAlt />
                                </div>
                                <span className="leading-relaxed">123 Pediatric Plaza<br/>Children's City, STATE 54321</span>
                            </div>
                            <div className="flex items-center gap-3 group">
                                <div className="p-2 rounded-lg bg-teal-900/50 text-teal-400 group-hover:bg-teal-500 group-hover:text-white transition-colors">
                                    <FaPhoneAlt />
                                </div>
                                <span>+1 (555) 123-4567</span>
                            </div>
                            <div className="flex items-center gap-3 group">
                                <div className="p-2 rounded-lg bg-teal-900/50 text-teal-400 group-hover:bg-teal-500 group-hover:text-white transition-colors">
                                    <FaEnvelope />
                                </div>
                                <span>hello@carecubs.com</span>
                            </div>
                        </div>
                    </div>

                    {/* Column 4: Newsletter & Social */}
                    <div className="flex flex-col gap-5">
                        <h3 className="text-white text-lg font-semibold tracking-wide">Stay Connected</h3>
                        <p className="text-sm text-teal-100/70 font-light">Subscribe to our newsletter for health tips and clinic updates.</p>
                        
                        <form className="relative flex flex-col gap-2 mt-1" onSubmit={(e) => e.preventDefault()}>
                            <div className="relative">
                                <input 
                                    type="email" 
                                    placeholder="Enter your email address" 
                                    className="w-full bg-slate-800/50 border border-teal-900/50 rounded-lg px-4 py-3 text-sm text-white placeholder:text-teal-100/30 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all backdrop-blur-sm"
                                />
                            </div>
                            <button 
                                type="button"
                                className="w-full bg-gradient-to-r from-teal-600 to-emerald-500 hover:from-teal-500 hover:to-emerald-400 text-white font-medium py-3 rounded-lg shadow-[0_0_15px_rgba(13,148,136,0.3)] hover:shadow-[0_0_20px_rgba(16,185,129,0.5)] transition-all duration-300 relative overflow-hidden group"
                            >
                                <span className="relative z-10">Subscribe</span>
                                <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent)] -translate-x-full group-hover:animate-[shimmer_1.5s_infinite] pointer-events-none"></div>
                            </button>
                        </form>

                        <div className="flex gap-3 mt-4">
                            {[FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn].map((Icon, i) => (
                                <a 
                                    key={i} 
                                    href="#" 
                                    className="w-10 h-10 rounded-full bg-slate-800/60 border border-teal-900/30 flex items-center justify-center text-teal-400 hover:bg-teal-500 hover:text-white hover:border-teal-400 hover:shadow-[0_0_15px_rgba(20,184,166,0.4)] transition-all duration-300 backdrop-blur-md hover:-translate-y-1"
                                >
                                    <Icon />
                                </a>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Subtle Wave Pattern Separator */}
                <div className="w-full h-px bg-gradient-to-r from-transparent via-teal-800 to-transparent mb-8"></div>

                {/* Copyright Bar */}
                <div className="flex flex-col md:flex-row justify-between items-center text-xs text-teal-100/50 font-light gap-4">
                    <p>&copy; {new Date().getFullYear()} CareCubs Clinic. All rights reserved.</p>
                    <div className="flex gap-6">
                        <Link href="#" className="hover:text-teal-300 transition-colors">Privacy Policy</Link>
                        <Link href="#" className="hover:text-teal-300 transition-colors">Terms of Service</Link>
                    </div>
                </div>
            </div>
        </footer>
    );
};

export default FooterLanding;
