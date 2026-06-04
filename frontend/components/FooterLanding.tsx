import Link from "next/link";
import Image from "next/image";
import { FaPhoneAlt, FaEnvelope, FaMapMarkerAlt, FaFacebookF, FaTwitter, FaInstagram, FaLinkedinIn } from "react-icons/fa";

const FooterLanding = () => {
    return (
        <footer className="bg-slate-900 text-gray-300 pt-16 pb-8 px-6 md:px-12 lg:px-24">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
                {/* Column 1: About */}
                <div className="flex flex-col gap-4">
                    <Link href="/">
                        <Image
                            className="w-48 object-contain filter brightness-0 invert"
                            src="/logoBig.png"
                            alt="Care Cubs Logo"
                            width={1080}
                            height={300}
                        />
                    </Link>
                    <p className="text-sm leading-relaxed mt-2 text-slate-400">
                        Expert pediatric care for your healthiest smile and happiest child. We provide compassionate, comprehensive medical services for infants, children, and adolescents.
                    </p>
                </div>

                {/* Column 2: Quick Links */}
                <div className="flex flex-col gap-4">
                    <h3 className="text-white text-lg font-semibold border-b border-slate-700 pb-2 mb-2 inline-block w-max">Quick Links</h3>
                    <div className="flex flex-col gap-3 text-sm">
                        <Link href="/" className="hover:text-orange-400 transition-colors">Home</Link>
                        <Link href="/#about" className="hover:text-orange-400 transition-colors">About Us</Link>
                        <Link href="/#services" className="hover:text-orange-400 transition-colors">Our Services</Link>
                        <Link href="/#doctors" className="hover:text-orange-400 transition-colors">Meet Our Doctors</Link>
                        <Link href="/Login" className="hover:text-orange-400 transition-colors">Patient Portal</Link>
                    </div>
                </div>

                {/* Column 3: Contact Info */}
                <div className="flex flex-col gap-4">
                    <h3 className="text-white text-lg font-semibold border-b border-slate-700 pb-2 mb-2 inline-block w-max">Contact Us</h3>
                    <div className="flex flex-col gap-4 text-sm">
                        <div className="flex items-start gap-3">
                            <FaMapMarkerAlt className="text-orange-500 mt-1 flex-shrink-0" />
                            <span>123 Pediatric Way, Suite 100<br/>Medical City, NY 10001</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <FaPhoneAlt className="text-orange-500 flex-shrink-0" />
                            <span>+1 (555) 123-4567</span>
                        </div>
                        <div className="flex items-center gap-3">
                            <FaEnvelope className="text-orange-500 flex-shrink-0" />
                            <span>hello@carecubs.com</span>
                        </div>
                    </div>
                </div>

                {/* Column 4: Newsletter / Social */}
                <div className="flex flex-col gap-4">
                    <h3 className="text-white text-lg font-semibold border-b border-slate-700 pb-2 mb-2 inline-block w-max">Connect With Us</h3>
                    <p className="text-sm text-slate-400 mb-2">Follow us on social media for health tips and clinic updates.</p>
                    <div className="flex gap-4">
                        <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-orange-500 hover:text-white transition-colors duration-300">
                            <FaFacebookF />
                        </a>
                        <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-orange-500 hover:text-white transition-colors duration-300">
                            <FaTwitter />
                        </a>
                        <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-orange-500 hover:text-white transition-colors duration-300">
                            <FaInstagram />
                        </a>
                        <a href="#" className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center hover:bg-orange-500 hover:text-white transition-colors duration-300">
                            <FaLinkedinIn />
                        </a>
                    </div>
                </div>
            </div>

            {/* Copyright Bar */}
            <div className="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center text-xs text-slate-500">
                <p>&copy; {new Date().getFullYear()} Care Cubs Pediatrics. All rights reserved.</p>
                <div className="flex gap-4 mt-4 md:mt-0">
                    <Link href="#" className="hover:text-gray-300 transition-colors">Privacy Policy</Link>
                    <Link href="#" className="hover:text-gray-300 transition-colors">Terms of Service</Link>
                </div>
            </div>
        </footer>
    );
};

export default FooterLanding;
