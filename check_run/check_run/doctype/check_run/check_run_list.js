frappe.listview_settings["Check Run"] = {
  add_fields: ["status"],
  hide_name_column: true,
  has_indicator_for_draft: 1,
  get_indicator: (doc) => {
    return [
      __(doc.status),
      {
        Draft: "red",
        Submitting: "orange",
        Submitted: "blue",
        "Ready to Print": "purple",
        "Confirm Print": "yellow",
        Printed: "green",
      }[doc.status],
      "status,=," + doc.status,
    ];
  },
};
