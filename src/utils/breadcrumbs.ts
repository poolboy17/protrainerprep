/**
 * Breadcrumb hierarchy for Pro Trainer Prep SEO pyramid.
 * Maps every article to: Home → Pillar → Hub → [Sub-Hub] → Page
 * 
 * Uses seoTier/seoParent frontmatter as source of truth.
 * This file is the runtime lookup for generating breadcrumb trails.
 */

interface BreadcrumbItem {
  label: string;
  href: string;
  tier?: string;
}

const PILLAR = {
  label: 'Become a Personal Trainer',
  href: '/guides/how-to-become-personal-trainer',
  tier: 'pillar',
};

// Hub definitions
const HUBS: Record<string, { label: string; href: string }> = {
  'career-change-fitness-guide': {
    label: 'Career Change Guide',
    href: '/career-change/career-change-fitness-guide',
  },
  'fitness-certification-guide': {
    label: 'Certification Guide',
    href: '/certifications/fitness-certification-guide',
  },
  'career-building-guide': {
    label: 'Career Building Guide',
    href: '/career-building/career-building-guide',
  },
  'ceu-recertification-guide': {
    label: 'CEU & Recertification',
    href: '/ceu/ceu-recertification-guide',
  },
};

// Complete pyramid: every slug → { tier, parentSlug, category }
const PYRAMID: Record<string, { tier: string; parent: string | null; category: string }> = {
  // Pillar
  "how-to-become-personal-trainer": { tier: "pillar", parent: null, category: "guides" },
  
  // Hubs
  "career-change-fitness-guide": { tier: "hub", parent: "how-to-become-personal-trainer", category: "career-change" },
  "fitness-certification-guide": { tier: "hub", parent: "how-to-become-personal-trainer", category: "certifications" },
  "career-building-guide": { tier: "hub", parent: "how-to-become-personal-trainer", category: "career-building" },
  "ceu-recertification-guide": { tier: "sub-hub", parent: "fitness-certification-guide", category: "ceu" },
  
  // Career Change spokes
  "career-change-fitness-after-40": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "career-change-fitness-after-50": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "best-cert-career-changers": { tier: "spoke", parent: "career-change-fitness-guide", category: "certifications" },
  "corporate-to-certified-timeline": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "is-it-too-late-to-become-personal-trainer": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "military-to-personal-trainer": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "nurse-to-personal-trainer": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "teacher-to-personal-trainer": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "personal-trainer-without-degree": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "gym-vs-independent-personal-trainer": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  "is-personal-training-good-career": { tier: "spoke", parent: "career-change-fitness-guide", category: "career-change" },
  
  // Certification spokes
  "ncsf-cpt-review": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "nasm-cpt-review": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "ace-cpt-review": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "issa-cpt-review": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "nasm-vs-ncsf": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "nasm-vs-ace": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "cheapest-personal-trainer-certifications": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "how-hard-is-personal-trainer-exam": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "ncsf-certification-renewal": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "ncsf-ceu-courses": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "nasm-recertification-cost": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "ace-recertification-cost": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "certification-expired-what-now": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "personal-trainer-certification-renewal": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "certified-nutrition-coach": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "strength-conditioning-coach-cscs-csc": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "prenatal-postpartum-training-certification": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "youth-fitness-certification": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "training-older-adults-certification": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "afford-fitness-certification": { tier: "spoke", parent: "fitness-certification-guide", category: "career-change" },
  "exercise-physiologist-vs-personal-trainer": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  "personal-trainer-nutrition-scope": { tier: "spoke", parent: "fitness-certification-guide", category: "certifications" },
  
  // CEU sub-hub spokes
  "best-online-ceu-providers": { tier: "spoke", parent: "ceu-recertification-guide", category: "ceu" },
  "cheapest-ceu-options": { tier: "spoke", parent: "ceu-recertification-guide", category: "ceu" },
  "free-ceus-personal-trainers": { tier: "spoke", parent: "ceu-recertification-guide", category: "ceu" },
  "fitness-conference-guide-ceus": { tier: "spoke", parent: "ceu-recertification-guide", category: "ceu" },
  
  // Career Building spokes
  "personal-trainer-salary": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "get-first-10-clients": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "personal-trainer-marketing": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "personal-training-pricing": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "personal-trainer-to-gym-manager": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "personal-trainer-100k": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "personal-trainer-niche-specialization": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "skills-certification-didnt-teach": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "alternative-careers-personal-trainers": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "part-time-personal-trainer": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "online-vs-in-person-personal-training": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "fitness-careers-no-gym": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "corporate-wellness-jobs-trainers": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
  "career-growth-guide": { tier: "spoke", parent: "career-building-guide", category: "career-building" },
};

function getUrl(slug: string): string {
  const entry = PYRAMID[slug];
  if (!entry) return `/${slug}`;
  return `/${entry.category}/${slug}`;
}

export function getBreadcrumbs(slug: string, title: string): BreadcrumbItem[] {
  const home: BreadcrumbItem = { label: 'Home', href: '/' };
  const entry = PYRAMID[slug];
  
  if (!entry) return [home, { label: title, href: `/${slug}` }];
  
  // Build chain by walking up parents
  const chain: BreadcrumbItem[] = [];
  let current = slug;
  
  while (current) {
    const e = PYRAMID[current];
    if (!e) break;
    
    const label = current === slug 
      ? title 
      : (HUBS[current]?.label || PILLAR.label);
    
    chain.unshift({ 
      label, 
      href: HUBS[current]?.href || getUrl(current),
      tier: e.tier 
    });
    
    current = e.parent || '';
  }
  
  return [home, ...chain];
}

export function getTier(slug: string): string {
  return PYRAMID[slug]?.tier || 'spoke';
}

export function getParentSlug(slug: string): string | null {
  return PYRAMID[slug]?.parent || null;
}

export function getSiblingSlugs(slug: string): string[] {
  const entry = PYRAMID[slug];
  if (!entry?.parent) return [];
  return Object.entries(PYRAMID)
    .filter(([s, e]) => e.parent === entry.parent && s !== slug)
    .map(([s]) => s);
}
