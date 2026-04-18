'use client';

import { useState, useEffect } from 'react';
import { MapPin, Star, Package, Clock } from 'lucide-react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Hero from '@/components/Hero';
import StickyCTA from '@/components/StickyCTA';
import ProductGallery from '@/components/ProductGallery';
import SocialProof from '@/components/SocialProof';
import StorySection from '@/components/StorySection';
import LocationPages from '@/components/LocationPages';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <StickyCTA />

      <main>
        {/* P09 + P13: Hero with 3-word messaging + anti-polish authenticity */}
        <Hero />

        {/* P19: StoryBrand section */}
        <StorySection />

        {/* P20: Menu galerie images (product catalog) */}
        <ProductGallery />

        {/* P02: Social proof adjacent to CTA */}
        <SocialProof />

        {/* P11: Location-based pages (multi-city) */}
        <LocationPages />
      </main>

      <Footer />
    </div>
  );
}
