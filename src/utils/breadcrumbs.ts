/**
 * Breadcrumb hierarchy mapper for Pro Trainer Prep.
 * Maps each post to its logical position in the 3-tier architecture:
 *   Home → Pillar → Sub-Hub → Spoke
 *
 * This follows LOGICAL hierarchy, not URL paths.
 */

interface BreadcrumbItem {
  label: string;
  href: string;
}

const PILLAR = {
  label: 'How to Become a Personal Trainer',
  href: '/blog/how-to-become-personal-trainer',
};

const HUBS: Record<string, { label: string; href: string; spokes: string[] }> = {
  certifications: {
    label: 'Certification Guide',
    href: '/blog/fitness-certification-guide',
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
    href: '/blog/career-change-fitness-guide',
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
    href: '/blog/career-building-guide',
    spokes: [
      'personal-trainer-salary',
      'get-first-10-clients',
    ],
  },
};

const HUB_SLUGS = Object.values(HUBS).map(h =>
  h.href.replace('/blog/', '')
);

export function getBreadcrumbs(slug: string, title: string): BreadcrumbItem[] {
  const home: BreadcrumbItem = { label: 'Home', href: '/' };

  // Is this the pillar page?
  if (slug === 'how-to-become-personal-trainer') {
    return [home, { label: title, href: PILLAR.href }];
  }

  // Is this a sub-hub page?
  for (const [, hub] of Object.entries(HUBS)) {
    const hubSlug = hub.href.replace('/blog/', '');
    if (slug === hubSlug) {
      return [home, PILLAR, { label: title, href: hub.href }];
    }
  }

  // It's a spoke — find its parent hub
  for (const [, hub] of Object.entries(HUBS)) {
    if (hub.spokes.includes(slug)) {
      return [
        home,
        PILLAR,
        { label: hub.label, href: hub.href },
        { label: title, href: `/blog/${slug}` },
      ];
    }
  }

  // Fallback: just Home → title
  return [home, { label: title, href: `/blog/${slug}` }];
}
