/**
 * Breadcrumb hierarchy mapper for Pro Trainer Prep.
 * Maps each post to its logical position in the 3-tier architecture:
 *   Home → Pillar → Sub-Hub → Spoke
 *
 * This follows LOGICAL hierarchy, not URL paths.
 * URLs use /%category%/%slug% pattern.
 */

interface BreadcrumbItem {
  label: string;
  href: string;
}

const PILLAR = {
  label: 'How to Become a Personal Trainer',
  href: '/guides/how-to-become-personal-trainer',
};

const HUBS: Record<string, { label: string; href: string; spokes: string[] }> = {
  certifications: {
    label: 'Certification Guide',
    href: '/certifications/fitness-certification-guide',
    spokes: [
      'ncsf-cpt-review',
      'nasm-cpt-review',
      'ace-cpt-review',
      'nasm-vs-ncsf',
      'nasm-vs-ace',
      'nasm-vs-ace-vs-issa',
      'cheapest-personal-trainer-certifications',
      'best-cert-career-changers',
      'best-certifications-second-career',
    ],
  },
  'career-change': {
    label: 'Career Change Guide',
    href: '/career-change/career-change-fitness-guide',
    spokes: [
      'is-it-too-late-to-become-personal-trainer',
      'fitness-careers-no-gym',
      'afford-fitness-certification',
      'corporate-to-certified-timeline',
      'career-change-fitness-after-40',
    ],
  },
  'career-building': {
    label: 'Career Building Guide',
    href: '/career-building/career-building-guide',
    spokes: [
      'personal-trainer-salary',
      'get-first-10-clients',
      'personal-training-pricing',
      'online-vs-in-person-personal-training',
      'personal-trainer-niche-specialization',
      'personal-trainer-marketing',
      'part-time-personal-trainer',
      'is-personal-training-good-career',
    ],
  },
};

// Map category to URL prefix
const CATEGORY_PREFIX: Record<string, string> = {
  guides: '/guides',
  certifications: '/certifications',
  'career-change': '/career-change',
  'career-building': '/career-building',
};

// Reverse lookup: spoke slug → category
const SPOKE_CATEGORY: Record<string, string> = {};
for (const [category, hub] of Object.entries(HUBS)) {
  for (const spoke of hub.spokes) {
    SPOKE_CATEGORY[spoke] = category;
  }
}

export function getBreadcrumbs(slug: string, title: string): BreadcrumbItem[] {
  const home: BreadcrumbItem = { label: 'Home', href: '/' };

  // Is this the pillar page?
  if (slug === 'how-to-become-personal-trainer') {
    return [home, { label: title, href: PILLAR.href }];
  }

  // Is this a sub-hub page?
  for (const [category, hub] of Object.entries(HUBS)) {
    const hubSlug = hub.href.split('/').pop() || '';
    if (slug === hubSlug) {
      return [home, PILLAR, { label: title, href: hub.href }];
    }
  }

  // It's a spoke — find its parent hub
  for (const [category, hub] of Object.entries(HUBS)) {
    if (hub.spokes.includes(slug)) {
      const prefix = CATEGORY_PREFIX[category] || '';
      return [
        home,
        PILLAR,
        { label: hub.label, href: hub.href },
        { label: title, href: `${prefix}/${slug}` },
      ];
    }
  }

  // Fallback: just Home → title
  return [home, { label: title, href: `/${slug}` }];
}
