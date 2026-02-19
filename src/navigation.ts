import { getPermalink, getBlogPermalink } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Become a Trainer',
      href: '/guides/how-to-become-personal-trainer',
    },
    {
      text: 'Certifications',
      href: '/certifications/fitness-certification-guide',
    },
    {
      text: 'Career Change',
      href: '/career-change/career-change-fitness-guide',
    },
    {
      text: 'Career Building',
      href: '/career-building/career-building-guide',
    },
    {
      text: 'Career Growth',
      href: '/career-growth/career-growth-guide',
    },
  ],
  actions: [{ text: 'Get Certified', href: '/certifications/fitness-certification-guide', variant: 'primary' }],
};

export const footerData = {
  links: [
    {
      title: 'Guides',
      links: [
        { text: 'Become a Personal Trainer', href: '/guides/how-to-become-personal-trainer' },
        { text: 'Certification Guide', href: '/certifications/fitness-certification-guide' },
        { text: 'Career Change Guide', href: '/career-change/career-change-fitness-guide' },
        { text: 'Career Building Guide', href: '/career-building/career-building-guide' },
        { text: 'Career Growth Guide', href: '/career-growth/career-growth-guide' },
      ],
    },
    {
      title: 'Popular Comparisons',
      links: [
        { text: 'NASM vs ACE vs ISSA', href: '/certifications/nasm-vs-ace-vs-issa' },
        { text: 'NASM vs NCSF', href: '/certifications/nasm-vs-ncsf' },
        { text: 'Cheapest Certifications', href: '/certifications/cheapest-personal-trainer-certifications' },
      ],
    },
    {
      title: 'Career Resources',
      links: [
        { text: 'Personal Trainer Salary', href: '/career-building/personal-trainer-salary' },
        { text: 'Get Your First 10 Clients', href: '/career-building/get-first-10-clients' },
        { text: 'NCSF CPT Review', href: '/certifications/ncsf-cpt-review' },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'About', href: getPermalink('/about') },
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
    { text: 'Terms of Service', href: getPermalink('/terms') },
    { text: 'Affiliate Disclosure', href: getPermalink('/affiliate-disclosure') },
  ],
  socialLinks: [
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: '/rss.xml' },
  ],
  footNote: `
    © ${new Date().getFullYear()} Pro Trainer Prep · All rights reserved.
  `,
};
