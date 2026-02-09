import { getPermalink, getBlogPermalink } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Become a Trainer',
      href: getPermalink('/blog/how-to-become-personal-trainer'),
    },
    {
      text: 'Certifications',
      href: getPermalink('/blog/fitness-certification-guide'),
    },
    {
      text: 'Career Change',
      href: getPermalink('/blog/career-change-fitness-guide'),
    },
    {
      text: 'Career Building',
      href: getPermalink('/blog/career-building-guide'),
    },
  ],
  actions: [],
};

export const footerData = {
  links: [
    {
      title: 'Guides',
      links: [
        { text: 'Become a Personal Trainer', href: getPermalink('/blog/how-to-become-personal-trainer') },
        { text: 'Certification Guide', href: getPermalink('/blog/fitness-certification-guide') },
        { text: 'Career Change Guide', href: getPermalink('/blog/career-change-fitness-guide') },
        { text: 'Career Building Guide', href: getPermalink('/blog/career-building-guide') },
      ],
    },
    {
      title: 'Popular Comparisons',
      links: [
        { text: 'NASM vs ACE vs ISSA', href: getPermalink('/blog/nasm-vs-ace-vs-issa') },
        { text: 'NASM vs NCSF', href: getPermalink('/blog/nasm-vs-ncsf') },
        { text: 'Cheapest Certifications', href: getPermalink('/blog/cheapest-personal-trainer-certifications') },
      ],
    },
    {
      title: 'Career Resources',
      links: [
        { text: 'Personal Trainer Salary', href: getPermalink('/blog/personal-trainer-salary') },
        { text: 'Get Your First 10 Clients', href: getPermalink('/blog/get-first-10-clients') },
        { text: 'NCSF CPT Review', href: getPermalink('/blog/ncsf-cpt-review') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
    { text: 'Terms of Service', href: getPermalink('/terms') },
  ],
  socialLinks: [
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: '/rss.xml' },
  ],
  footNote: `
    © ${new Date().getFullYear()} Pro Trainer Prep · All rights reserved.
  `,
};
